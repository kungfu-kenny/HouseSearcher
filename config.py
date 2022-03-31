import os
from dotenv import load_dotenv


load_dotenv()

class Folders:
    folder_main = os.getcwd()
    folder_logs = 'logs'
    folder_storage = 'storage'
    folder_results = 'dataframe'

class WebDriver:
    link = os.getenv("WEBDRIVER_LINK")
    folder = 'webdriver'
    name = 'chromedriver'
    name_archive = 'selenium_name.zip'
    remove = False

class WebFlatfy:
    name = 'flatfy'
    time_wait = 10
    link_start = 'https://flatfy.ua'
    link_continue = 'аренда-квартир-киев'

class WebOlx:
    name = 'olx'
    time_wait = 10
    link_start = 'https://www.olx.ua'
    link_continue = 'https://www.olx.ua/nedvizhimost/kvartiry/dolgosrochnaya-arenda-kvartir/kiev'
    
class WebRieltor:
    name = 'rieltor'
    time_wait = 10
    link_start = 'https://rieltor.ua'
    link_continue = 'https://rieltor.ua/flats-rent/'

class WebDomria:
    name = 'domria'
    time_wait = 10
    link_start = 'https://dom.ria.com'
    link_continue = 'https://dom.ria.com/uk/'
    list_check = 'Списком'
    rent_status = 'Орендувати квартиру'

class Address:
    name = 'adress'
    time_wait = 10
    time_sleep = 1
    link_start = 'https://address.ua'
    rent_status = 'Снять'
    city_kyiv = 'киев'

class Message:
    message_click = 'Clicked to search results'
    message_city = 'Added city to the search results'
    message_status_rent = 'Added rent status to the results'
    message_price = 'Added price to the search results'
    message_district = 'Added dictrict to the search results'
    message_rooms = 'Added several rooms to the search results'
    message_insert_text = 'Add inserted text to it'
    message_finish_settings = 'Finished the search settings'
    message_done = 'Done with search'
    message_done_tr = 'Done with data transformation to the file'
    message_city_basic = 'Added city on the start page by clicking on it'
    message_markup_success = 'Added check of the right markup and everything is okay'
    message_markup_fail = 'Added check of the right markup and we need change it'
    message_markup_change = 'Added the type of the markup'