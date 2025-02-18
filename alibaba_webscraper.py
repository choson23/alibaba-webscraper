from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Configuración del WebDriver
driver = webdriver.Chrome()
url = "https://zzmuduo.en.alibaba.com/productgrouplist-812671707-1/Chicken_Equipment.html?filter=null&spm=a2700.shop_plgr.41413.dbtmnavgo"
driver.get(url)

# Obtener cookies de Selenium
cookies = driver.get_cookies()

# Usar una sesión de requests para mantener las cookies
session = requests.Session()
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Añadir headers para simular un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Referer': url
}

# Crear directorio base para guardar las imágenes
base_dir = 'images_alibaba'
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

page_number = 1

while True:
    # Obtener todos los enlaces ANTES de visitar cualquier producto
    product_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'title-link icbu-link-normal')]")
    urls = [link.get_attribute("href") for link in product_links if link.get_attribute("href")]

    for product_url in urls:
        if not product_url:
            print("Advertencia: Se encontró un enlace sin URL, saltando...")
            continue

        print(f"Visitando: {product_url}")
        driver.get(product_url)
        time.sleep(random.uniform(2, 4))  # Pequeña pausa para evitar detección

        # Intentar aceptar cookies si aparece el botón
        try:
            cookie_button = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'gdpr-btn gdpr-agree-btn')]"))
            )
            cookie_button.click()
        except:
            pass  # Si no aparece, continuar

        # Obtener nombre del producto
        try:
            elemento = driver.find_element(By.XPATH, "//h1[@title]")
            nombre_producto = elemento.get_attribute("title").strip()
        except:
            nombre_producto = "producto_desconocido"

        # Crear carpeta para el producto
        individual_folder = os.path.join(base_dir, nombre_producto)
        if not os.path.exists(individual_folder):
            os.makedirs(individual_folder)

        # Descargar imágenes
        try:
            imagenes = WebDriverWait(driver, 5).until(
                EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'id-h-full id-w-full id-object-contain')]"))
            )

            print(f"Se encontraron {len(imagenes)} imágenes para {nombre_producto}.")

            for idx, imagen in enumerate(imagenes):
                img_url = imagen.get_attribute("src")
                if img_url:
                    img_data = session.get(img_url, headers=headers).content
                    with open(os.path.join(individual_folder, f'{page_number}-{idx}.jpg'), 'wb') as img_file:
                        img_file.write(img_data)
                    print(f'Imagen {idx + 1} guardada en {individual_folder}.')
                    time.sleep(random.uniform(1, 3))
        except:
            print("No se encontraron imágenes en este producto.")

        # Regresar a la página principal para procesar el siguiente enlace
        driver.back()
        time.sleep(random.uniform(2, 4))

    try:
        # Intentar hacer clic en el botón "Siguiente"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'next-btn next-btn-normal next-btn-medium next-pagination-item')]"))
        )
        next_button.click()
        time.sleep(random.uniform(3, 6))
        page_number += 1
    except:
        print("No hay más páginas.")
        break

# Cerrar el navegador
driver.quit()
