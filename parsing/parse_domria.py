from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from config import WebDomria, Message

class ParseDomria(ParseMain):
    """
    class which is dedicated to parse the domria website and return selected values
    """
    def __init__(self, driver_path: str, insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseDomria, self).__init__(driver_path)
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
        Method which is dedicated to work with th
        """
        self.get('https://dom.ria.com')#/uk/arenda-kvartir/kiev/')
        print('dsssssssssssssssssssssssssssssss')
        # item-pseudoselect pointer
        value_check = self.find_element_by_css_selector('div.item-pseudoselect.pointer')
        print(value_check)
        value_check.click()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
        
        for f in self.find_elements(By.CSS_SELECTOR, 'div.item'):
            if f.text == 'Орендувати квартиру':
                print(f.text)
                print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@')
                f.click()
                break
        
        value_input = self.find_element_by_css_selector('input#autocomplete')
        print(value_input)
        value_input.click()
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<,')
        
        #TODO change here of the change development
        value_input.send_keys('Київ, Київська область')
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        value_input.send_keys(Keys.ENTER)
        print('ccccccccccccccccccccccccccccccccccccccccccccccc')

        value_check = self.find_element_by_css_selector('a.flex.f-space.f-center.button-search')
        # print(value_check)
        value_check.click()

        # k = self.find_element_by_id('autocomplete')
        # print(k)
        # print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        # k.send_keys('Київ')
        # print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        # # k.submit()
        # k.send_keys(Keys.ENTER)
        # print('33333333333333333333333333333')

        # self.find_element_by_id('autocomplete-1').click()
        # print('cccccccccccccccccccccccccccccccccccccccccccccccccccccc')
        
        # for types in self.find_elements_by_css_selector('label.tabs-item'):
        #     if types.text == 'Оболонський':
        #         types.click()
        #         break
        # print('?>????????????????????????????????????????????????????????????????')
        # self.find_element_by_id('autocomplete-1').send_keys('мінська')
        
        # #TODO change here to explicit wait
        # for f in self.find_elements_by_class_name('item'):
        #     if 'мінська' in f.text.lower():
        #         f.click()
        #         break

        #TODO change here to explicit wait
        # self.find_element_by_id('mainAdditionalParams_0').find_element(By.CSS_SELECTOR,'div.first-letter.overflowed.greyChars').click()
        self.find_element(By.CSS_SELECTOR,'div.first-letter.overflowed.greyChars').click()
        # before = self.find_element_by_id('235_from')
        # print(before)
        # before.send_keys('0')
        # print('0')
        after = self.find_element_by_id('235_to')
        print(after)
        after.send_keys('20000')
        print(20000)
        # self.find_element_by_id('235_to').send_keys(Keys.RETURN)
        # self.find_element_by_css_selector('div.search-popups.options').click()
        # self.find_element_by_css_selector('div.button-search.flex.f-center.f-text-c.small').click()
        self.find_element_by_id('mainAdditionalParams_0').find_element(By.CSS_SELECTOR,'div.first-letter.overflowed.greyChars').click()
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

        self.find_element_by_css_selector('div#mainAdditionalParams_1').find_element(By.CSS_SELECTOR,'div.first-letter.overflowed.greyChars').click()
        # self.find_element(By.CSS_SELECTOR,'div.item-pseudoselect.form-selected.small').click()
        # print(self.find_elements_by_css_selector('div.item-pseudoselect.form-selected.small'))
        # print('xxxxxccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc')
        # print(self.find_elements_by_css_selector('div.item-pseudoselect.form-selected.small')[1])
        #.click()
        import time
        time.sleep(5)