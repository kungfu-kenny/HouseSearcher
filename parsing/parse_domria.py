from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from config import WebDomria, Message

class ParseDomria(ParseMain):
    """
    class which is dedicated to parse the domria website and return selected values
    """
    def __init__(self, driver_path: str, insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseMain, self).__init__(driver_path)
        self.used_db = WebDomria.name
        self.web = WebDomria.link_start
        self.link = WebDomria.link_continue
        self.text = insert
        self.district = district
        self.price_bool = bool(price)
        self.price =price
        self.list_rooms = self.produce_list_rooms(rooms)

    @staticmethod
    def produce_list_rooms(rooms) -> list:
        """
        
        """
        pass

    def produce_search_city(self) -> None:
        """
        
        """
        pass

    def produce_search_district(self) -> None:
        """
        
        """
        pass

    def produce_search_rooms(self) -> None:
        """
        
        """
        pass

    def produce_search_result_click(self) -> None:
        """
        
        """
        pass

    # d

    def produce_search_results(self) -> None:
        """
        
        """
        self.get('https://dom.ria.com/uk/arenda-kvartir/kiev/')
        k = self.find_element_by_css_selector('div.flex.w80u')
        print(k)
        print('dsssssssssssssssssssssssssssssss')
        z = k.find_element(By.CSS_SELECTOR, 'div.item-pseudoselect.form-selected.small')
        # item-pseudoselect form-selected small
        print(z)
        print('ggggggggggggggggggggggggggggggggggggggggg')
        z.click()
        # search-popups options
        # indent
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        v = self.find_element_by_css_selector('div.search-popups.options')
        print(v)
        # v.click()
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        c = v.find_elements(By.CSS_SELECTOR, 'div.group-class.chars-row-235-246')# 'input.elem.col2')
        print(c)