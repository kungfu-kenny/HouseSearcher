import os
from dotenv import load_dotenv


load_dotenv()

class Folders:
    folder_main = os.getcwd()
    folder_storage = 'storage'
    folder_results = 'dataframe'

class WebDriver:
    link = os.getenv("WEBDRIVER_LINK")
    folder = 'webdriver'
    name = 'chromedriver'
    name_archive = 'selenium_name.zip'
    remove = False

class WebOlx:
    time_wait = 30
    link = 'https://www.olx.ua/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev'
    