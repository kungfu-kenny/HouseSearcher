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
        self.price = price
        self.list_rooms = self.produce_list_rooms(rooms)

    @staticmethod
    def produce_list_rooms(rooms) -> list:
        """
        Method which is dedicated to work with the
        Input:  rooms = list with the int room values
        Output: we developed the selected values
        """
        return [str(f) for f in rooms]

    def produce_rent_status(self) -> None:
        """
        Method which is dedicated to add the rent status to the beginning of the search
        Input:  None
        Output: we developed the adding to the rent status
        """
        self.find_element_by_css_selector('div.item-pseudoselect.pointer').click()
        for f in self.find_elements(By.CSS_SELECTOR, 'div.item'):
            if f.text == 'Орендувати квартиру':
                f.click()
                break

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to add the price status of the search
        Input:  None
        Output: we developed the price filter
        """
        WebDriverWait(self, 5).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div#mainAdditionalParams_0'
                )
            )
        )
        
        WebDriverWait(self, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    'div.first-letter.overflowed.greyChars'
                )
            )
            and EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div.first-letter.overflowed.greyChars'
                )
            )
        ).click()
        
        after = WebDriverWait(self, 5).until(
            EC.presence_of_element_located(
                (
                    By.ID, 
                    '235_to'
                )
            )
        )
        after.send_keys('20000')
        
        WebDriverWait(self, 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    'button.button-search.flex.f-center.f-text-c.small.boxed'
                )
            )
        ).click()

    def produce_search_city_basic(self)-> None:
        """
        Method which is dedicated to work with the search
        Input:  None
        Output: we developed if necessary 
        """
        value_input = self.find_element_by_css_selector('input#autocomplete')
        value_input.click()
        #TODO change here to the non basic
        value_input.send_keys('Київ, Київська область')
        value_input.send_keys(Keys.ENTER)

    def produce_search_city(self) -> None:
        """
        Method which is dedicated to add search of the city
        Input:  values of the inserted city
        Output: we developed the city search for the flat
        """
        #TODO add after here checkings
        k = self.find_element_by_id('autocomplete')
        #TODO add here the selected values
        k.send_keys('Київ')
        k.send_keys(Keys.ENTER)

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to produce the district of the selected
        Input:  values of the inserted city
        Output: we developed the district searched for the flat
        """
        pass

    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to add filters for the searched rooms
        Input:  None
        Output: we developed the rooms searches
        """
        WebDriverWait(
            self.find_element_by_css_selector('div#mainAdditionalParams_1'), 5).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    'div.first-letter.overflowed.greyChars'
                )
            )
        )
        self.find_element_by_css_selector(
            'div#mainAdditionalParams_1'
        ).find_element(
                By.CSS_SELECTOR,
                'div.first-letter.overflowed.greyChars'
            ).click()
        
        for element in self.find_elements_by_css_selector('label.tabs-item'):
            if element.text:
                if element.text in ['2', '3']:
                    element.click()
        
        self.find_element_by_css_selector(
            'div#mainAdditionalParams_1'
        ).find_element(
                By.CSS_SELECTOR,
                'button.button-search.flex.f-center.f-text-c.small.boxed'
            ).click()
        
    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to produce the search button click after the all filters
        Input:  None
        Output: we developed the click for the search
        """
        self.find_element_by_css_selector('a.flex.f-space.f-center.button-search').click()

    def produce_search_type_markup_check(self) -> bool:
        """
        Method which is dedicated to work with the markup selected
        Input:  None
        Output: we developed the check the values
        """
        return self.find_element_by_css_selector('button.button-border.small.active.noClickEvent').text == 'Списком'

    def produce_search_type_markup(self) -> None:
        """
        Method which is dedicated to produce the list values of the filtration
        Input:  None
        Output: we developed the type of the selected markup which would be shown
        """
        for f in WebDriverWait(self, 5).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR, 
                    'button.button-border.small'
                )
            )
        ):
            if f.text == 'Списком':
                f.click()

    def wait_loading_elements(self) -> None:
        """
        Method which is dedicated to develop the load waiting for all values
        Input:  None
        Output: we produced the waiting to the wait of the selected elements
        """
        pass

    def produce_search_results(self) -> None:
        """
        Method which is dedicated to work with th
        """
        self.get(WebDomria.link_start)
        
        self.produce_rent_status()
        #TODO add here the logger
        print('We added rent status')
        
        self.produce_search_city_basic()
        #TODO add here the logger
        print('We added basic city to this value')
        
        self.produce_search_result_click()
        #TODO add here the logger
        print('We added click on the search button')
        
        if self.produce_search_type_markup_check():
            #TODO add here logger
            print('We added check of the right markup and everything is okay')
        else:
            #TODO add here logger
            print('We added check of the right markup and we need change it')
            self.produce_search_type_markup()
            print('We added the type of the markup')
            

        if self.price_bool:
            self.produce_search_city()
            #TODO add here the logger
            print('We added city to this value')

        self.produce_search_price()
        #TODO add here logger
        print('We added the price to this value')

        self.produce_search_rooms()
        #TODO add here logger
        print('We added the rooms to this value')

        import time
        time.sleep(5)

        return

        # self.find_element_by_id('autocomplete-1').click()
        
        # WebDriverWait(self, 5).until(
        #     EC.element_to_be_clickable(
        #         (
        #             By.CSS_SELECTOR, 
        #             'label#geo-box'#'input#autocomplete-1' #item-pseudoselect autocomplete-open
        #         )
        #     )
        # )
        # print(14)
        # self.find_element_by_css_selector('input#autocomplete-1').click()
        # print('cccccccccccccccccccccccccccccccccccccccccccccccccccccc')
        
        # for types in self.find_elements_by_css_selector('label.tabs-item'):
        #     if types.text == 'Оболонський':
        #         types.click()
        #         break
        # print('?>????????????????????????????????????????????????????????????????')
        # self.find_element_by_id('autocomplete-1').send_keys('мінська')
        
        
        # print('5555555555555555555555555555555')
        # for f in WebDriverWait(self, 5).until(
        #     EC.presence_of_all_elements_located(
        #         (
        #             By.CLASS_NAME, 
        #             'item'
        #         )
        #     )
        # ):
        #     if 'мінська' in f.text.lower():
        #         f.click()
        #         break
        # print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        
        # self.find_element(By.CSS_SELECTOR,'div.first-letter.overflowed.greyChars').click()

        #TODO add here values to wait
        # self.implicitly_wait(5)
        # self.find_elements_by_css_selector('button.button-border.small')[1].click()
        print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')

        value_price = [f.text for f in self.find_elements_by_css_selector('b.size18')]
        pprint(value_price)

        value_links = [f.get_attribute('href') for f in self.find_elements_by_css_selector('a.realty-link.size22.bold.mb-10.break.b')]
        pprint(value_links)

        value_adress = [f.text for f in self.find_elements_by_css_selector('a.realty-link.size22.bold.mb-10.break.b')]
        pprint(value_adress)

        print('>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')
        print(len(value_price), len(value_links), len(value_adress))

        # span mb-5 grey -> address accurate
        # span mt-10 chars grey -> room parameters
        # mt-15 text pointer desc-hidden -> desc
        # size14 flex mt-10 -> datetime
        # flex f-center b grey mt-10 -> subway to check

        import time
        time.sleep(5)