from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from config import WebRieltor, Message


class ParseRieltor(ParseMain):
    """
    class which is dedicated to parse the rieltor website
    """
    def __init__(self, driver_path: str, insert:str='', district:str='', rooms:list=[], price:int=0, currency:str='uah') -> None:
        super(ParseRieltor, self).__init__(driver_path)
        self.used_db = WebRieltor.name
        self.web = WebRieltor.link_start
        self.text_insert = insert
        self.text_district = district
        self.list_rooms = [str(i) for i in rooms]
        self.check_district = bool(self.text_district)
        self.check_text = bool(self.text_insert)
        self.currency = currency
        self.currency_bool = self.currency == 'uah'
        self.price_bool = bool(price)
        self.price = self.produce_price_value(price, self.currency)

    @staticmethod
    def produce_price_value(price:int, currency:str='uah') -> str:
        """
        Static method which is dedicated to develop the price selected
        Input:  price = value of selected prices to check flat
                currency = currency to check
        Output: string which is dedicated to get on click
        """
        if price < 10000 and currency == 'uah':
            return 'до 10 000 грн/міс'
        elif 10000 <= price < 15000 and currency == 'uah':
            return 'від 10 000 до 15 000 грн/міс'
        elif 15000 <= price < 30000 and currency == 'uah':
            return 'від 15 000 до 30 000 грн/міс'
        elif price >= 30000 and currency == 'uah':
            return 'від 30 000 грн/міс'
        elif price < 350 and currency != 'uah':
            return 'до 350 $/міс'
        elif 350 <= price < 500 and currency != 'uah':
            return 'від 350 до 500 $/міс'
        elif 500 <= price < 1000 and currency != 'uah':
            return 'від 500 до 1 000 $/міс'
        elif price >= 1000 and currency != 'uah':
            return 'від 1 000 $/міс'


    def produce_search_city(self) -> None:
        """
        Method which is dedicated to develop search of the city
        Input:  None
        Output: we developed the search of the selected city
        """
        self.find_element_by_css_selector('input.nav_item_input_active').click()
        for element in self.find_elements_by_css_selector("div.nav_item_option_geo_city.js_nav_input"):
            if element.text == 'Київ':
                element.click()
                break

    def produce_rent_status(self) -> None:
        """
        Method which is dedicated to develop the rent value
        Input:  None
        Output: we developed the rent mode on the website
        """
        self.find_element_by_css_selector('div.nav_item_active_wr.js_open_nav').click()
        for element in self.find_elements_by_css_selector('div.nav_item_option.js_nav_option'):
            if element.text == 'Оренда квартир':
                element.click()
                break

    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to search on the room numbers within the house
        Input:  None
        Output: we developed the number of rooms for it
        """
        value_cube = self.wait_loading_elements('div.nav_items_wrap')[0].find_element(By.CSS_SELECTOR, 'div.nav_items_wr')
        self.execute_script(
            "arguments[0].click();",
            value_cube.find_element(
                By.CSS_SELECTOR, 
                'div.nav_item_active_wr.js_open_nav'
            )
        )
        for element in WebDriverWait(
            value_cube, WebRieltor.time_wait).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.CSS_SELECTOR, 
                        'div.nav_item_option.js_nav_option_many'
                        )
                    )
                ):
            if element.text in self.list_rooms:
                self.execute_script(
                    "arguments[0].click();",
                    element
                )

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to develop prices of the selected values
        Input:  None
        Output: we developed the price values which could be used
        """
        value_cube = self.find_element_by_css_selector('div.nav_items_wr.nav_items_wr_middle')
            # WebDriverWait(self, WebRieltor.time_wait).until(
            #     EC.presence_of_element_located(
            #         (
            #             By.CSS_SELECTOR, 
            #             'div.nav_items_wr.nav_items_wr_middle'
            #         )
            #     )
            # )
        print(value_cube)
        self.execute_script(
            "arguments[0].click();",
            value_cube.find_element('div.nav_item_active_wr.js_open_nav')
        )
        print('dfsaaaaaadffdfdfdfdf')
        # for element in value_cube.find_elements(By.CSS_SELECTOR, 'div.nav_item_option.js_nav_option'):
        # WebDriverWait(
        #         value_cube, WebRieltor.time_wait).until(
        #         EC.presence_of_all_elements_located(
        #             (
        #                 By.CSS_SELECTOR, 
        #                 'div.nav_item_option.js_nav_option'
        #                 )
        #             )
        #         ):
            # if element.text == self.price:
            #     print(element.text)
            #     element.click()
            #     print('dsadsadasdadas')
            
    def produce_search_district(self) -> None:
        """
        Method which is dedicated to produce the selected district
        Input:  None
        Output: we developed the values of selected district & text
        """
        input_text = self.find_element_by_css_selector('input.nav_street_input')
        input_text.click()
        if self.check_text:
            input_text.send_keys(self.text_insert)
        if self.check_district:
            for element, but in zip(
                self.find_elements_by_css_selector('div.nav_item_option_rayon.js_nav_rayon'), 
                self.find_elements_by_css_selector('div.nav_item_rayon_checkbox')):
                if element.text == self.text_district:
                    but.click()
                    break

    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to produce the search button click
        Input:  None
        Output: we develop the search button 
        """
        self.find_element_by_css_selector('button.nav_search_btn').click()

    def wait_loading_elements(self, value_element:str="div.catalog-item__info") -> None:
        """
        Method which is dedicated to develop the load of the 
        Input:  value_element = element which is required to wait
        Output: we waited to load elements
        """
        return WebDriverWait(self, WebRieltor.time_wait).until(
            EC.visibility_of_all_elements_located(
                (
                    By.CSS_SELECTOR, 
                    value_element
                    )
                )
            )

    def develop_values_further(self, value_input:int=1) -> bool:
        """
        Method which is dedicated to check that it was left some values
        Input:  value_input = int value which is now value
        Output: we developed the link or false to search values
        """
        for k, link in [[f.text, f.get_attribute('href')] for f in self.find_elements_by_css_selector('a.pager-btn')]:
            if str(value_input + 1) == k:
                return link
        return False

    def produce_search_elements_empty(self, empty_search:str) -> list:
        """
        Method which is dedicated to develop the search elements of unneccessary element
        Input:  empty_search = element of the selected 
        Output: we developed the list of this values
        """
        value_return = []
        for f in self.wait_loading_elements():
            k = f.find_elements(By.CSS_SELECTOR, empty_search)
            if k:
                value_return.append(k[0].text)
            else:
                value_return.append('')
        return value_return

    def produce_search_results(self) -> list:
        """
        Method which is dedicated to return values of the results by the flats
        """
        self.get(WebRieltor.link_continue)
        
        self.produce_search_city()
        self.produce_log(Message.message_city)

        self.produce_rent_status()
        self.produce_log(Message.message_status_rent)        

        #TODO deal with this after
        # if self.price_bool:
        #     self.produce_search_price()
        #     self.produce_log(Message.message_price)

        if self.check_district or self.check_text:
            self.produce_search_district()        
            if self.check_district:
                self.produce_log(Message.message_district)
            if self.check_text:
                self.produce_log(Message.message_insert_text)

        if self.list_rooms:  
            self.produce_search_rooms()
            self.produce_log(Message.message_rooms)

        self.produce_search_result_click()
        self.produce_log(Message.message_click)
        
        self.wait_loading_elements()
        print(Message.message_finish_settings)
        
        streets = [f.text for f in self.wait_loading_elements('div.catalog-item__title_street')]
        
        links = [
            f.find_element(By.TAG_NAME, 'a').get_attribute('href') 
            for f in self.find_elements_by_css_selector('h2.catalog-item__title')
        ]
        
        districts = [
            f.text 
            for f in self.find_elements_by_css_selector('div.catalog-item__title_district')
        ]
        
        prices = [
            f.text 
            for f in self.find_elements_by_css_selector('strong.catalog-item__price')
        ]
        
        subways = self.produce_search_elements_empty(
            'a.label.label_location.label_location_subway')
        
        types = self.produce_search_elements_empty(
            'span.label.label_attention')
        
        commission = self.produce_search_elements_empty(
            'span.label.label_no_commission')
        
        values = self.produce_search_elements_empty(
            'div.catalog-item_info-item-row')
        
        descriptions = self.produce_search_elements_empty(
            'p.catalog-item_info-item-row.catalog-item_info-description')
        
        value_ind = 1
        value_now = self.develop_values_further(value_ind)

        while value_now:
            self.produce_log(f'We found the other variations, check the {value_ind + 1} page')
            self.get(value_now)
            self.wait_loading_elements()
            
            streets.extend(
                [f.text for f in self.find_elements_by_css_selector('div.catalog-item__title_street')]
            )
            
            links.extend(
                [f.find_element(By.TAG_NAME, 'a').get_attribute('href') 
                for f in self.find_elements_by_css_selector('h2.catalog-item__title')]
            )
            
            districts.extend(
                [f.text for f in self.find_elements_by_css_selector('div.catalog-item__title_district')]
            )
            
            prices.extend(
                [f.text for f in self.find_elements_by_css_selector('strong.catalog-item__price')]
            )
            
            subways.extend(
                self.produce_search_elements_empty('a.label.label_location.label_location_subway')
            )

            types.extend(
                self.produce_search_elements_empty('span.label.label_attention')
            )

            commission.extend(
                self.produce_search_elements_empty('span.label.label_no_commission')
            )

            values.extend(
                self.produce_search_elements_empty('div.catalog-item_info-item-row')
            )

            descriptions.extend(
                self.produce_search_elements_empty('p.catalog-item_info-item-row.catalog-item_info-description')
            )
            
            value_ind += 1
            value_now = self.develop_values_further(value_ind)

        self.produce_log(Message.message_done)
        print(
                len(streets), 
                len(links), 
                len(districts), 
                len(prices), 
                len(subways), 
                len(types), 
                len(commission), 
                len(values), 
                len(descriptions)
            )
        print('===============================================================================')
        self.produce_log(Message.message_done_tr)
            