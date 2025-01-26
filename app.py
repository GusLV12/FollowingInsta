from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
import os
import time
import pandas as pd
from datetime import datetime

# Cargar las variables del archivo .env
dotenv_path = os.path.join(os.path.dirname(__file__), "env", ".env")
load_dotenv(dotenv_path)

username = os.getenv("IG_NAME")
password = os.getenv("IG_PSSD")


print(f"Username: {username}")
print(f"Password: {password}")

# Ruta relativa basada en el directorio actual del script
driver_path = os.path.join(os.path.dirname(__file__), "drivers", "msedgedriver.exe")

def login_to_instagram():
    print("Logging in to Instagram...")
    if not username or not password:
        raise ValueError("Please add your username and password in the .env file")
    
    # Configuración del navegador para Microsoft Edge
    edge_options = Options()
    edge_options.use_chromium = True  # Indica que Edge usa Chromium
    edge_options.add_argument('--start-maximized')

    # Crear el servicio para Edge WebDriver
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)

    print("Initiating the browser...")
    try:
        driver.get("https://www.instagram.com/")
        print("Instagram login page loaded.")
        username_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']"))
        )
        username_input.send_keys(username)
        password_input = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        password_input.send_keys(password)
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
    except Exception as e:
        print(f"Failed to load Instagram: {e}")
        driver.quit()
        raise

    return driver

if __name__ == "__main__":
    driver = login_to_instagram()
    input("Press Enter to close the browser...")
    
