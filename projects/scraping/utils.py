import logging
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager

from config import HEADLESS, BROWSER, USER_AGENT

def ensure_dir(path: str) -> None:
    """Creates the folder if does not exist"""
    os.makedirs(path, exist_ok=True)

def get_driver(headless: bool = HEADLESS, browser: str = BROWSER, user_agent: str = USER_AGENT):
    browser = browser.lower()

    if browser == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument("--start-maximized")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--mute-audio")
        options.add_argument("--log-level=3")
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.add_argument(f"user-agent={user_agent}")

        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)

    elif browser == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.set_preference("general.useragent.override", user_agent)

        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    elif browser == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless=new")
        options.add_argument(f"user-agent={user_agent}")

        try:
            service = EdgeService(EdgeChromiumDriverManager().install())
        except Exception as e:
            logging.error(f"Error dowloading Edge driver: {e}")
            raise

        return webdriver.Edge(service=service, options=options)

    elif browser == "safari":
        if headless:
            logging.warning("⚠️ Safari does not support headless. Running in normal mode.")
        logging.warning("⚠️ Safari does not support changing user-agent via Selenium.")
        return webdriver.Safari()

    else:
        raise ValueError(f"Browser does not soport: {browser}")