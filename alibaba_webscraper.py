from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuración del WebDriver
driver = webdriver.Chrome()  # Cambia a tu navegador si es necesario
url = "https://zzmuduo.en.alibaba.com/productgrouplist-812671707/Equipo_de_pollo.html"
driver.get(url)

# Obtener cookies de Selenium
cookies = driver.get_cookies()

# Usar una sesión de requests para mantener las cookies
session = requests.Session()

# Añadir cookies a la sesión
for cookie in cookies:
    session.cookies.set(cookie['name'], cookie['value'])

# Añadir headers a la solicitud para simular un navegador real
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36',
    'Referer': url
}

# Hacemos click en la X para evitar el pop-up
try:
    dismiss_button = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-tracking-control-name, 'public_jobs_contextual-sign-in-modal_modal_dismiss')]"))
    )
    dismiss_button.click()
except Exception as e:
    print("No pop-up to dismiss.")

# Crear directorio para guardar las imágenes
if not os.path.exists('images'):
    os.makedirs('images')

page_number = 1

while True:
    # Esperar hasta que los elementos del álbum estén presentes
    albums = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//img[@loading='lazy']"))
    )

    # Comprobar si la variable albums tiene elementos
    if albums:
        print(f"Se encontraron {len(albums)} elementos en la página {page_number}.")
    else:
        print("No se encontraron elementos en esta página.")

    # Descargar imágenes
    for idx, album in enumerate(albums):
        img_url = album.get_attribute('src')
        img_data = session.get(img_url, headers=headers).content
        with open(f'images/page_{page_number}_image_{idx}.jpg', 'wb') as img_file:
            img_file.write(img_data)
        print(f'Imagen {idx} de la página {page_number} descargada.')

    # Intentar encontrar el botón "Siguiente" y hacer clic en él
    try:
        next_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Next') or contains(text(), 'Siguiente')]"))
        )
        next_button.click()
        time.sleep(3)  # Esperar para cargar la siguiente página
        page_number += 1
    except Exception as e:
        print("No se encontró un botón 'Siguiente' o ya no hay más páginas.")
        break

# Cerrar el navegador
driver.quit()
