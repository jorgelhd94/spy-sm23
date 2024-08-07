from datetime import timedelta
from apps.product.models import Category, Product, Provider, Shop
from django.db.models import Q, F, Value, FloatField, ExpressionWrapper
from django.db.models.functions import Replace, Trim
from django.db.models.expressions import Func
from django.db import models
from functools import reduce
import re
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.utils import timezone

from apps.statistics_spy.models import ProductsUpdateLogs


class Unaccent(Func):
    function = 'unaccent'
    output_field = models.CharField()


def get_product_queryset(query_params, exclude_categories: bool = False, exclude_manufactures: bool = False):
    search_text = query_params.get('q', '')
    offers = query_params.get('offers', '')
    discounts = query_params.get('discounts', '')
    orderby = query_params.get('orderby', 'default')
    mode = query_params.get('mode', 'show_all')
    price_by_weight = query_params.get('price_by_weight', 'show_all')
    provider = query_params.get('provider', '')
    category = query_params.get('category', '')
    manufactures = query_params.get('manufactures', '')
    min_price = query_params.get('min_price', '')
    max_price = query_params.get('max_price', '')

    products_queryset = full_search_products(
        search_text) if search_text else Product.objects.all()
    

    # Filtrar productos actualizados después de la última actualización exitosa
    try:
    # Obtén los productos cuyo updated_at es mayor que date_last_update de su tienda
        products_queryset = products_queryset.filter(
            models.Q(updated_at__gt=models.F('shop__date_last_update')) | models.Q(shop__date_last_update__isnull=True)
        )
    except Shop.DoesNotExist:
        pass  # No hay tiendas registradas


    # Offers
    if offers:
        offer_datetime = timezone.now() - timedelta(days=int(offers))
        products_queryset = products_queryset.filter(
            previous_price_updated_at__gte=offer_datetime.date(),
            previous_price__gt=F('current_price')
        )

    # Discounts
    if discounts:
        discount_percentage = float(discounts) / 100
        products_queryset = products_queryset.filter(
            Q(current_price__lte=F('old_price') * (1 - discount_percentage)) |
            Q(current_price__lte=F('previous_price') * (1 - discount_percentage))
        )

    if not exclude_categories:
        # Clean Name
        products_queryset = get_products_cleaned_name(
            products_queryset
        )

        # Order By
        products_queryset = sort_products(products_queryset, orderby)

    # Mode
    products_queryset = filter_products_by_mode(
        products_queryset, mode)

    # Price By Weight
    products_queryset = filter_by_price_weight(
        products_queryset, price_by_weight)

    # Filter by provider
    if provider:
        provider = Provider.objects.get(pk=provider)
        products_queryset = products_queryset.filter(provider=provider)

    # Filter by category
    if category:
        try:
            category = Category.objects.get(pk=category)
            categories_list = [category] + category.get_descendants()
            products_queryset = products_queryset.filter(
                categories__in=categories_list)
        except Category.DoesNotExist:
            products_queryset = products_queryset.none()

    # Filter by manufactures
    if manufactures and not exclude_manufactures:
        manufacture_ids_list = manufactures.split(",")
        products_queryset = products_queryset.filter(
            manufacture__id__in=manufacture_ids_list)

    # Prices
    try:
        if min_price:
            min_price = float(min_price)
            products_queryset = products_queryset.filter(
                current_price__gte=min_price)
    except:
        pass

    try:
        if max_price:
            max_price = float(max_price)
            products_queryset = products_queryset.filter(
                current_price__lte=max_price)
    except:
        pass

    return products_queryset


def sort_products(products_queryset, orderby):
    order_mapping = {
        'default': 'cleaned_name',          # Por ranking
        'less_price': 'current_price',    # Menor precio
        'higher_price': '-current_price',  # Mayor precio
        'new': '-created_at',        # Más nuevo
        'less_price_by_weight': 'price_by_weight',  # Menor precio/lb
        'less_discount': 'discount_percentage',    # Menor descuento
        'higher_discount': '-discount_percentage'  # Mayor descuento
    }

    try:
        if orderby == 'default':
            products_queryset = products_queryset.order_by('-rank')
        elif orderby in ['less_discount', 'higher_discount']:
            discount_percentage = ExpressionWrapper(
                (F('old_price') - F('current_price')) / F('old_price') * 100,
                output_field=FloatField()
            )
            products_queryset = products_queryset.annotate(
                discount_percentage=discount_percentage
            ).exclude(old_price__isnull=True)  # Excluye los productos sin old_price
            products_queryset = products_queryset.order_by(
                order_mapping.get(orderby, 'discount_percentage')
            )
        else:
            products_queryset = products_queryset.order_by(
                order_mapping.get(orderby, 'cleaned_name'))
    except Exception as e:
        # En caso de error, ordenamos por nombre
        products_queryset = products_queryset.order_by(
            order_mapping.get(orderby, 'cleaned_name'))

    return products_queryset


def search_products(query):
    search_words = query.split()
    # Normalizar el término de búsqueda
    unaccented_search_words = [Unaccent(Value(word)) for word in search_words]

    unaccented_query = reduce(
        lambda q, word: q & Q(unaccent_name__icontains=word),
        unaccented_search_words,
        Q()
    )

    products_queryset = Product.objects.annotate(
        unaccent_name=Unaccent(Replace(Replace(Replace(Trim(F('name')), Value(
            '\t'), Value('')), Value('\r'), Value('')), Value('\n'), Value('')))
    ).filter(unaccented_query)

    return products_queryset


def full_search_products(query):
    filtered_words = [word for word in query.split() if len(
        word) >= 4 and not re.search(r'\d', word)]

    if len(filtered_words) >= 2:
        search_query = SearchQuery(filtered_words[0], config='spanish')
        for word in filtered_words[1:]:
            search_query |= SearchQuery(word, config='spanish')
    else:
        return search_products(query)

    search_vector = SearchVector('name', config='spanish')

    products_queryset = Product.objects.annotate(
        rank=SearchRank(search_vector, search_query),
    ).filter(rank__gte=0.03).order_by("-rank")

    if products_queryset.count() == 0:
        products_queryset = search_products(query)

    return products_queryset


def filter_by_price_weight(products_queryset, param):
    if not param in ['with_price_weight', 'without_price_weight']:
        return products_queryset

    if param == 'with_price_weight':
        products_queryset = products_queryset.filter(
            Q(price_by_weight__isnull=False) | Q(price_by_weight__gt=0))

    if param == 'without_price_weight':
        products_queryset = products_queryset.filter(
            Q(price_by_weight__isnull=True) | Q(price_by_weight__lt=0))

    return products_queryset


def is_combo_product(product):

    regex = re.compile(r'\(\b\d+ x +\b\d* +[a-zA-Z]*', re.IGNORECASE)

    if regex.search(product.name):
        return True

    if 'combo' in product.name.lower():
        return True

    descendant_category_ids = get_descendant_category_ids('Combos')

    if product.categories.filter(id__in=descendant_category_ids).exists():
        return True

    return False


def filter_products_by_mode(products_queryset, mode):
    if mode in ['combo', 'simple']:
        # Obtén las IDs de las categorías descendientes de 'Combos'
        descendant_category_ids = get_descendant_category_ids(
            'Combos')

        # Filtra los productos por el nombre que incluya "Combo"
        combo_name_filtered_ids = filter_products_by_combo_name(
            products_queryset)

        # Incluye productos cuyo nombre contenga "Combo"
        products_with_combo_in_name = products_queryset.filter(
            name__icontains='Combo').values_list('id', flat=True)

        # Agrega los IDs de los productos con "Combo" en el nombre a los IDs filtrados por nombre de combo
        combo_name_filtered_ids = list(
            set(combo_name_filtered_ids).union(set(products_with_combo_in_name)))

        if mode == 'combo':
            products_queryset = products_queryset.filter(
                Q(categories__id__in=descendant_category_ids) | Q(
                    id__in=combo_name_filtered_ids)
            )
        elif mode == 'simple':
            products_queryset = products_queryset.exclude(
                Q(categories__id__in=descendant_category_ids) | Q(
                    id__in=combo_name_filtered_ids)
            )

    return products_queryset


def get_valid_page(request, query_params, paginator, products_queryset_count):
    # Validar página proporcionada
    page_number = query_params.get(paginator.page_query_param, 1)

    try:
        page_number = int(page_number) if int(page_number) > 0 else 1
    except:
        page_number = 1

    page_size = paginator.get_page_size(request)
    total_items = products_queryset_count
    total_pages = (total_items + page_size - 1) // page_size

    if page_number > total_pages:
        return 1

    return page_number


def get_descendant_category_ids(category_name):
    try:
        category = Category.objects.get(name=category_name)
        descendant_categories = category.get_descendants()
        descendant_category_ids = [
            category.id for category in descendant_categories]
        descendant_category_ids.append(category.id)
        return descendant_category_ids
    except Category.DoesNotExist:
        return []


def filter_products_by_combo_name(products_queryset):
    regex = re.compile(r'\(\b\d+ x +\b\d* +[a-zA-Z]*', re.IGNORECASE)
    filtered_products = []

    for product in products_queryset:
        if regex.search(product.name):
            filtered_products.append(product.id)

    return filtered_products


def get_products_cleaned_name(products_queryset: models.QuerySet):
    return products_queryset.annotate(
        cleaned_name=Trim(
            Replace(
                Replace(
                    Replace(F('name'), Value('\t'), Value('')),
                    Value('\r'), Value('')
                ),
                Value('\n'), Value(''),
            )
        )
    )


def get_ranked_products_sm23(product: Product):
    ranked_products = full_search_products(
        product.name).order_by('current_price')

    ranked_products = get_products_cleaned_name(
        ranked_products)

    if is_combo_product(product):
        ranked_products = filter_products_by_mode(
            ranked_products, 'combo')
    else:
        ranked_products = filter_products_by_mode(
            ranked_products, 'simple')

    min_price = product.current_price * 0.5
    max_price = product.current_price * 1.5
    ranked_products = ranked_products.filter(
        current_price__gte=min_price, current_price__lte=max_price)

    return ranked_products


def filterCategoriesByParams(category: Category):
    pass
