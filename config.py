import os
from dotenv import load_dotenv


load_dotenv()

class Lang:
    ukr = 'ukr'
    rus = 'rus'

class Default:
    price = 0
    rooms = []
    insert = ''
    district = ''
    city_ukr = 'київ'
    city_rus = 'киев'

class DefaultDict:
    value_city_ukr_rus = {
        Default.city_ukr:Default.city_rus,
        Default.city_rus:Default.city_rus,
    }
    value_city_rus_ukr = {
        Default.city_ukr:Default.city_ukr,
        Default.city_rus:Default.city_ukr,
    }
    value_district_ukr_rus = {
        'оболонський':'оболонский',
        'оболонский':'оболонский',
        'голосіївський':'голосеевский',
        'голосеевский':'голосеевский',
        'дарницкий':'дарницкий',
        'дарницький':'дарницкий',
        'деснянский':'деснянский',
        'деснянський':'деснянский',
        'днепровский':'днепровский',
        'дніпровський':'днепровский',
        'печерський':'печерский',
        'печерский':'печерский',
        'подольский':'подольский',
        'подольський':'подольский',
        'святошинский':'святошинский',
        'святошинський':'святошинский',
        'шевченковский':'шевченковский',
        'шевченківський':'шевченковский',
        "солом'янський":'соломенский',
        "соломенский":'соломенский',
    }
    value_district_rus_ukr = {
        'оболонський':'оболонський',
        'оболонский':'оболонський',
        'голосеевский':'голосіївський',
        'голосіївський':'голосіївський',
        'дарницкий':'дарницький',
        'дарницький':'дарницький',
        'деснянский':'деснянський',
        'деснянський':'деснянський',
        'днепровский':'дніпровський',
        'дніпровський':'дніпровський',
        'печерський':'печерський',
        'печерский':'печерський',
        'подольский':'подольський',
        'подольський':'подольський',
        'святошинский':'святошинський',
        'святошинський':'святошинський',
        'шевченковский':'шевченківський',
        'шевченківський':'шевченківський',
        "солом'янський":"солом'янський",
        "соломенский":"солом'янський",
    }

class Folders:
    file_json = 'default.json'
    file_default_data = 'data.json'
    folder_main = os.getcwd()
    folder_logs = 'logs'
    folder_json = 'json'
    folder_storage = 'storage'
    folder_results = 'results'

class Columns:
    column_name = 'Name'
    column_link = 'Link'
    column_date = 'Datetime Updated'
    column_price = 'Price'
    column_desc = 'Description'
    column_rooms = 'Room Number'
    column_square = 'Square'
    column_subway = 'Subway'
    column_square_price = 'Square Price'
    column_square_split = 'Square Splited'
    column_floor = 'Floor'
    column_address = 'Address'
    column_subdists = 'Subdistrict'
    column_commission = 'Commission'
    column_types = 'House Project Type'
    column_types_site = 'Website Type'
    column_types_repair = 'Repairment Type'
    column_address_name = 'Address Name'
    column_address_number = 'Address Number'
    column_address_add = 'Address Additional'
    column_date_created = 'Created At'

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
    name = 'address'
    time_wait = 10
    time_sleep = 0.5
    link_start = 'https://address.ua'
    rent_status = 'Снять'
    city_kyiv = Default.city_rus

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
    message_mistake = 'We faced mistake with this unstable elements'
    message_empty = 'Unfortunately we have problems with the df size so we return empty'