import logging
from datetime import datetime
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from utils import get_driver, ensure_dir
from config import BASE_URL, PAGES_TO_SCRAPE

def scrape_news() -> tuple[pd.DataFrame, str]:

    # Timestamps for naming
    ts_file = datetime.now().strftime("%Y%m%d_%H%M%S")  

    # Screenshots folder
    screenshot_folder = f"screenshots/scraping_{ts_file}"
    ensure_dir(screenshot_folder)

    logging.info("Starting WebDriver...")
    driver = get_driver()

    data = []

    try:
        for page in range(PAGES_TO_SCRAPE):
            logging.info(f"Scraping page {page + 1}...")

            url = BASE_URL if page == 0 else f"{BASE_URL}?p={page + 1}"
            logging.info(f"Open URL: {url}")
            driver.get(url)

            # Wait until at least one article link is present
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".titleline a"))
            )

            # Extract data
            for item in driver.find_elements(By.CSS_SELECTOR, ".titleline a"):
                data.append({
                    "title": item.text,
                    "link": item.get_attribute("href"),
                    "scraping_date": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
                })

            # Save screenshots by page
            screenshot_path = f"{screenshot_folder}/hackernews_page{page+1}_{ts_file}.png"
            driver.save_screenshot(screenshot_path)
            logging.info(f"Screenshot guardado en {screenshot_path}")

    finally:
        driver.quit()
        logging.info("WebDriver closed.")

    # Convert list of dictionaries to a pandas DataFrame
    df = pd.DataFrame(data)
    return df, screenshot_folder