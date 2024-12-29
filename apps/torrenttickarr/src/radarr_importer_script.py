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


# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)
chrome_options.add_argument("--no-sandbox")  # Required for running Chrome in Docker
chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional but often needed in headless mode)

# Path to chromedriver
chrome_driver_path = '/usr/local/bin/chromedriver'


# Function to log in to the page
def autoimport_radarr():
    # Set up Chrome WebDriver
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Navigate to the initial URL
        driver.get("https://radarr.internal.dbcloud.org/activity/queue")

        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://radarr.internal.dbcloud.org/activity/queue")
        )
        
        # Ensure the page is loaded by waiting for a visible table element
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//table"))
        )

        # Get the number of rows in the table
        rows = driver.find_elements(By.XPATH, "//table/tbody/tr")
        row_count = len(rows)

        for i in range(1, row_count + 1):  # Use index-based iteration
            try:
                # Re-locate the first icon in the last column for the current row
                icon_xpath = f"//table/tbody/tr[{i}]/td[last()]//button[1]"
                icon = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, icon_xpath))
                )

                icon.click()
                time.sleep(2)  # Wait for modal to appear

                # Find and click the import button in the modal
                import_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'Modal-modal')]//button[contains(text(), 'Import')]"))
                )
                import_button.click()
                time.sleep(2)  # Wait for import action to complete

                logging.info(f'Processed row {i} successfully.')

            except Exception as row_error:
                logging.error(f"Error processing row {i}: {row_error}")
                continue

        logging.info('Auto-import process completed successfully')

    except Exception as e:
        logging.error(f'Login failed due to an exception: {e}')
    finally:
        # Close the browser session
        driver.quit()


# Run the login function for different websites
if __name__ == "__main__":
    autoimport_radarr()