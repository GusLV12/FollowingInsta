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

# Funciones de default
def format_to_international(value):
    if value == '': return 0

    number = int(float(value) * 1000)
    return number


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
        time.sleep(5)
    except Exception as e:
        print(f"Failed to load Instagram: {e}") 
        driver.quit()
        raise

    return driver

def get_followers(driver, username):
    print(f"Getting followers of {username}...")
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(5)  # Dar tiempo a la página para cargar

    try:
        # Buscar el enlace de "Seguidores" y extraer el número de seguidores
        followers_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href='/{username}/followers/'] span[title]"))
        )
        followers_count = followers_link.get_attribute("title")
        print(f"{username} tiene {followers_count}")
        followers_count = format_to_international(followers_count)
        print(f"{username} tiene {followers_count} seguidores")
        followers_link.click()
        time.sleep(3)

        followers_xpath = '/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]'
        follow_count = '_ap3a._aaco._aacw._aacx._aad7._aade'

        follows = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, followers_xpath))
        )

        # Scroll to the end of the followers list
        hour = datetime.now()
        diff_hour = datetime.now() - hour
        seconds_scroll = diff_hour.total_seconds()
        fol_find = 0

        while followers_count > fol_find and seconds_scroll < 60:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follows)
            time.sleep(1)
            fol_find = len(follows.find_elements(By.CLASS_NAME, follow_count))
            diff_hour = datetime.now() - hour
            seconds_scroll = diff_hour.total_seconds()

        my_followers = driver.find_elements(By.CLASS_NAME, follow_count)
        print(f"Found {len(my_followers)} followers")

        seguidores = []
        for seguidor in my_followers:
            seguidores.append(seguidor.text)

        return seguidores
    
    except Exception as e:
        print(f"Error finding followers count: {e}")
        driver.quit()
        raise

def get_following(driver, username):
    print(f"Getting following of {username}...")
    driver.get(f"https://www.instagram.com/{username}/")
    time.sleep(5)  # Dar tiempo a la página para cargar

    try:
        # Buscar el enlace de "Seguidores" y extraer el número de seguidores
        followers_link = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, f"a[href='/{username}/following/']"))
        )
        followers_count = followers_link.get_attribute("title")
        print(f"{username} tiene {followers_count}")
        followers_count = format_to_international(followers_count)
        print(f"{username} tiene {followers_count} siguiendo")
        followers_link.click()
        time.sleep(3)

        followers_xpath = "/html/body/div[5]/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]"
        follow_count = '_ap3a._aaco._aacw._aacx._aad7._aade'

        follows = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, followers_xpath))
        )

        # Scroll to the end of the followers list
        hour = datetime.now()
        diff_hour = datetime.now() - hour
        seconds_scroll = diff_hour.total_seconds()
        fol_find = 0

        while followers_count > fol_find and seconds_scroll < 60:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", follows)
            time.sleep(1)
            fol_find = len(follows.find_elements(By.CLASS_NAME, follow_count))
            diff_hour = datetime.now() - hour
            seconds_scroll = diff_hour.total_seconds()

        my_followers = driver.find_elements(By.CLASS_NAME, follow_count)
        print(f"Found {len(my_followers)} followers")

        seguidos = []
        for seguidor in my_followers:
            seguidos.append(seguidor.text)

        return seguidos
    
    except Exception as e:
        print(f"Error finding following count: {e}")
        driver.quit()
        raise


def save_to_excel(lista, column, followers=None):
    df = pd.DataFrame(lista, columns=[column])

    if column == 'Seguidos' and followers is not None:
        df['Me sigue'] = df[column].apply(lambda x: 'Si' if x in followers else 'No')
    
    filename = f'{column}.xlsx'
    df.to_excel(filename, index=False)
    print(f"Saved to {filename}")
    return filename

if __name__ == "__main__":
    driver = login_to_instagram()
    followers = get_followers(driver, "xchronofox")
    following = get_following(driver, "xchronofox")
    excel_file = save_to_excel(followers, 'Seguidores')
    escel_file = save_to_excel(following, 'Seguidos', followers)
    input("Press Enter to close the browser...")
    
