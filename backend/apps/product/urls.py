from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'manufactures', views.ManufactureViewSet)
router.register(r'categories', views.CategoryViewSet, basename='category')
router.register(r'providers', views.ProviderViewSet)
# router.register(r'comparison_zones', ComparisonZoneViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('product-ranking/<int:product_id>/',
         views.ProductRankView.as_view(), name='product-ranking'),
    path('products/<int:pk>/related/',
         views.RelatedProductsView.as_view(), name='product-related'),
    path('products/<int:product_id>/price-history/',
         views.PriceHistoryListView.as_view(), name='price-history-list'),
    path('categories-menu/',
         views.CategoryAPIView.as_view(), name='categories-menu'),
    path('manufactures-list/',
         views.ManufactureAPIView.as_view(), name='manufactures-list'),
    path('products-test/',
         views.ProductTestView.as_view(), name='product-test'),
    path('cat-test/',
         views.CategoryKataTestView.as_view(), name='category-kata-test'),
    path('kata-products-test/',
         views.ProductsKataTestView.as_view(), name='products-kata-test'),
    path('sm23-products-test/',
         views.ProductsSm23TestView.as_view(), name='products-sm23-test'),
    path('tuambia-products-test/',
         views.ProductsTuAmbiaTestView.as_view(), name='tuambia-sm23-test'),
    path('duplicate-items/',
         views.SearchDuplicateItems.as_view(), name='duplicate-items'),
]
