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
    albums = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@class, 'product-image')]"))
    )
    product_links = driver.find_elements(By.XPATH, "//a[contains(@class, 'title-link icbu-link-normal')]")
    

    for link in product_links:
        product_url = link.get_attribute("href")
        if product_url:
            print(product_url)
            driver.get(product_url)
            time.sleep(2)
        else:
            print("Advertencia: Se encontró un enlace sin URL")
            continue

        # Intentar capturar el botón de cookies y hacer clic, pero continuar si no se encuentra
        try:
            cookie_producto = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'gdpr-btn gdpr-agree-btn')]"))
            )
            driver.execute_script("arguments[0].click();", cookie_producto)
        except Exception as e:
            print("No se encontró el botón de cookies, continuando el proceso.")
        #buscamos el nombre del producto
        elemento = driver.find_element(By.XPATH, "//h1[@title]")
        nombre_producto = elemento.get_attribute("title")  # O, alternativamente: nombre_producto = elemento.text
       

        imagenes = WebDriverWait(driver, 5).until(
            EC.presence_of_all_elements_located((By.XPATH, "//img[contains(@class, 'id-h-full id-w-full id-object-contain')]")))

        if imagenes:
            print(f"Se encontraron {len(imagenes)} elementos en el album del articulo.")
        else:
            print("No se encontraron elementos en esta página.")

        for idx, (imagen) in enumerate(imagenes):
            img_url = imagen.get_attribute("src")
            img_data = session.get(img_url, headers=headers).content

            # Crear carpeta dentro de 'images_alibaba'
            individual_folder = os.path.join(base_dir, nombre_producto)
            if not os.path.exists(individual_folder):
                os.makedirs(individual_folder)

            with open(os.path.join(individual_folder, f'{page_number}-{idx}.jpg'), 'wb') as img_file:
                img_file.write(img_data)
            print(f'Imagen {idx} de la página {page_number} descargada en {individual_folder}.')
            time.sleep(random.uniform(1, 3))

    try:
        # Desplazar hacia abajo para hacer visible el botón "Siguiente"
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Esperar un poco para permitir la carga

        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'next-btn next-btn-normal next-btn-medium next-pagination-item')]")
        ))
        next_button.click()
        time.sleep(random.uniform(3, 6))
        page_number += 1
    except Exception as e:
        print("No se encontró un botón 'Siguiente' o ya no hay más páginas.")
        break

# Cerrar el navegador
driver.quit()
