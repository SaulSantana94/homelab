from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import logging
import time

# Configure the logging system to log to stdout
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Environment variables for secrets
USERNAME = os.getenv('USERNAME')
PASSWORD_HDO = os.getenv('PASSWORD_HDO')
PASSWORD_TORRENTEROS = os.getenv('PASSWORD_TORRENTEROS')
PASSWORD_TORRENTLAND = os.getenv('PASSWORD_TORRENTLAND')
PASSWORD_TORRENTLEECH = os.getenv('PASSWORD_TORRENTLEECH')

# Set up Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Required for running Chrome in Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but often needed in headless mode)

# Path to chromedriver
chrome_driver_path = '/usr/local/bin/chromedriver'


# Function to log in to the page
def login_hdo():
    # Set up Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the initial URL
        driver.get("https://hd-olimpo.club/login")

        # Find the username and password fields and fill them in
        user_field = driver.find_element(By.ID, "username")
        pass_field = driver.find_element(By.ID, "password")

        user_field.send_keys(USERNAME)

        # Wait for 2 seconds
        time.sleep(2)
        
        pass_field.send_keys(PASSWORD_HDO)
        # Wait for 2 seconds
        time.sleep(2)

        # Some websites require clicking a login button
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Wait for the URL to change to the expected URL
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://hd-olimpo.club/pages/1")
        )

        # Check if the current URL is the expected URL
        current_url = driver.current_url
        if current_url == "https://hd-olimpo.club/pages/1":
            logging.info('Login successful. Redirected to %s', current_url)
        else:
            logging.error('Login failed. Current URL is %s', current_url)

    except Exception as e:
        logging.error(f'Login failed due to an exception: {e}')
    finally:
        # Wait for 2 seconds
        time.sleep(2)
        # Close the browser session
        driver.quit()

def login_torrenteros():
    # Set up Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the initial URL
        driver.get("https://torrenteros.org/login")

        # Find the username and password fields and fill them in
        user_field = driver.find_element(By.NAME, "username")
        pass_field = driver.find_element(By.NAME, "password")

        user_field.send_keys(USERNAME)

        # Wait for 2 seconds
        time.sleep(2)
        
        pass_field.send_keys(PASSWORD_TORRENTEROS)
        
        # Wait for 2 seconds
        time.sleep(2)

        # Some websites require clicking a login button
        login_button = driver.find_element(By.XPATH, "//button[@class='auth-form__primary-button']")
        login_button.click()

        # Wait for the URL to change to the expected URL
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://torrenteros.org/pages/1")
        )

        # Check if the current URL is the expected URL
        current_url = driver.current_url
        if current_url == "https://torrenteros.org/pages/1":
            logging.info('Login successful. Redirected to %s', current_url)
        else:
            logging.error('Login failed. Current URL is %s', current_url)

    except Exception as e:
        logging.error(f'Login failed due to an exception: {e}')
    finally:
        # Wait for 2 seconds
        time.sleep(2)
        # Close the browser session
        driver.quit()


def login_torrentland():
    # Set up Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the initial URL
        driver.get("https://torrentland.li/login")

        # Find the username and password fields and fill them in
        user_field = driver.find_element(By.ID, "username")
        pass_field = driver.find_element(By.ID, "password")

        user_field.send_keys(USERNAME)

        # Wait for 2 seconds
        time.sleep(2)
        
        pass_field.send_keys(PASSWORD_TORRENTLAND)

        # Wait for 2 seconds
        time.sleep(2)
        
        # Some websites require clicking a login button
        login_button = driver.find_element(By.ID, "login-button")
        login_button.click()

        # Wait for the URL to change to the expected URL
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://torrentland.li/")
        )

        # Check if the current URL is the expected URL
        current_url = driver.current_url
        if current_url == "https://torrentland.li/":
            logging.info('Login successful. Redirected to %s', current_url)
        else:
            logging.error('Login failed. Current URL is %s', current_url)

    except Exception as e:
        logging.error(f'Login failed due to an exception: {e}')
    finally:
        # Wait for 2 seconds
        time.sleep(2)
        # Close the browser session
        driver.quit()


def login_torrentleech():
    # Set up Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the initial URL
        driver.get("https://www.torrentleech.org/user/account/login/")

        # Find the username and password fields and fill them in
        user_field = driver.find_element(By.NAME, "username")
        pass_field = driver.find_element(By.NAME, "password")

        user_field.send_keys(USERNAME)

        # Wait for 2 seconds
        time.sleep(2)
        
        pass_field.send_keys(PASSWORD_TORRENTLEECH)
        
        # Wait for 2 seconds
        time.sleep(2)

        # Some websites require clicking a login button
        login_button = driver.find_element(By.XPATH, "//button[@type='submit' and contains(@class, 'tl-btn') and contains(@class, 'btn-primary')]")
        login_button.click()

        # Wait for the URL to change to the expected URL
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://www.torrentleech.org/torrents/top/index/added/-1%20day/orderby/completed/order/desc")
        )

        # Check if the current URL is the expected URL
        current_url = driver.current_url
        if current_url == "https://www.torrentleech.org/torrents/top/index/added/-1%20day/orderby/completed/order/desc":
            logging.info('Login successful. Redirected to %s', current_url)
        else:
            logging.error('Login failed. Current URL is %s', current_url)

    except Exception as e:
        logging.error(f'Login failed due to an exception: {e}')
    finally:
        # Wait for 2 seconds
        time.sleep(2)
        # Close the browser session
        driver.quit()

# Run the login function for different websites
if __name__ == "__main__":
    login_hdo()
    login_torrenteros()
    login_torrentland()
    login_torrentleech()