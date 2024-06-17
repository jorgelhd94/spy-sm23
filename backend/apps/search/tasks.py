from common.libs.selenium import SeleniumDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from apps.product.models import Product, Category
from apps.statistics_spy.models import ProductsUpdateLogs

from django.utils import timezone
from django.db.models import Count

from common.stores.sm23 import scraper_sm23

import time


def update_database_sm23():
    print("Iniciando...")
    seleniumDriver = SeleniumDriver()
    base_url = ""

    now = timezone.now()

    update = ProductsUpdateLogs(
        start_time=now,
        status='processing'
    )
    update.save()
    
    try:
        new_products_count = 0
        updated_products_count = 0
        scraper_sm23.create_categories(seleniumDriver, base_url)

        categories = Category.objects.annotate(num_sub_cat=Count('children')).filter(num_sub_cat=0)

        print(f"Categorias a procesar: {categories.count()}\n")

        for category in categories:
            base_url = "categoria/" + category.category_id
            total = scraper_sm23.create_or_update_products(seleniumDriver, base_url, category)

            print('------------------------')
            print(f'Categoria procesada: {category.name}')
            print(f'Cantidad de productos: {total}')
            print('------------------------\n')


        new_products = Product.objects.filter(created_at__gte=now)
        new_products_count = new_products.count()

        updated_products = Product.objects.filter(updated_at__gte=now).exclude(created_at__gte=now)
        updated_products_count = updated_products.count()

        deleted_products = Product.objects.filter(updated_at__lt=now)
        deleted_products_count = deleted_products.count()

        update.end_time = timezone.now()
        update.status = 'success'
        update.new_products_count = new_products_count
        update.updated_products_count = updated_products_count
        update.deleted_products_count = deleted_products_count

    except Exception as e:
        print("Ocurrió un error:", e)
        update.end_time = timezone.now()
        update.status = 'error'
        update.note = str(e)
    finally:
        print("Terminado")
        seleniumDriver.quit()
        update.save()

    return {"proceso": "Terminado"}


def test_auth():
    seleniumDriver = SeleniumDriver()

    try:
        driver = seleniumDriver.get_driver("autenticar")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username")))
        time.sleep(2)

        # Encuentra los campos de entrada y el botón de inicio de sesión
        email_field = driver.find_element(By.NAME, "username")
        password_field = driver.find_element(By.NAME, "password")
        login_button = driver.find_element(By.XPATH, "//button[@type='submit']")

        email_field.send_keys("jorgelhd94@gmail.com")
        password_field.send_keys("Jlhd*940830")

        login_button.click()

        time.sleep(4)
    except Exception as e:
        print("Ocurrió un error:", e)
    finally:
        seleniumDriver.quit()

