# We import the right libraries 
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
from selenium.webdriver.support.ui import WebDriverWait


# Configuracion del WebDriver y del Enlace
driver = webdriver.Chrome() # Cambia a tu navegador si es necesario
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
    'Referer': url}


# Hacemos click en la X para evitar el pop-up
# Esperar hasta que el botón de cierre esté presente
"""dismiss_button = WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.XPATH, "//button[contains(@data-tracking-control-name, 'public_jobs_contextual-sign-in-modal_modal_dismiss')]"))
)"""

# Hacer clic en el botón
#dismiss_button.click()

