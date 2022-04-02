import time
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from config import Message, Address


class ParseAddress(ParseMain):
    """
    class which is dedicated to develop the parsing of the adress
    """
    def __init__(self, driver_path:str, city:str='', insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseAddress, self).__init__(driver_path)
        self.city = Address.city_kyiv if not city else city
        self.price_bool = bool(price)
        self.price, self.price_click = self.produce_price_value(price)
        self.district = district.lower()
        self.rooms = self.produce_list_rooms(rooms)

    @staticmethod
    def produce_price_value(price:int) -> list:
        """
        Static method which is dedicated to produce the price value
        Input:  price = selected price value which was used
        Output: string to use the price and boolean value
        """
        if price < 4000:
            return 'до 4000 грн.', True
        elif 4000 <= price < 8000:
            return 'до 8000 грн.', True
        elif 8000 <= price < 15000:
            return 'до 15000 грн.', True
        return price, False

    @staticmethod
    def produce_list_rooms(rooms:list) -> list:
        """
        Static method which is dedicated to get the list of rooms
        Input:  rooms = list of the rooms to use
        Output: list of the rooms to use
        """
        return [str(room) for room in rooms]

    @staticmethod
    def produce_chunks(value_list:list, n:int=6) -> list:
        """
        Static method which is dedicated to work with a chunk of list value
        Input:  value_list = list of the selected values
                n = length of the chunk
        Output: 
        """
        def chunks(lst:list, n:int) -> list:
            for i in range(0, len(lst), n):
                yield lst[i:i + n]
        return list(chunks(value_list, n))

    def produce_rent_status(self) -> None:
        """
        Method which is dedicated to develop the rent status for it
        Input:  None
        Output: we developed the rent status for change
        """
        if self.find_element_by_css_selector('li.tab.pointer.active').text == Address.rent_status:
            return
        for element in self.find_elements_by_css_selector('li.tab.pointer'):
            if element.text.strip() == Address.rent_status:
                element.click()
                break
    
    def produce_check_kyiv_development(self, value_default:list=[Address.city_kyiv]) -> bool:
        """
        Method which is dedicated to check that it is kyiv developed
        Input:  value_default
        Output: boolean value which is about check that we are using the kyiv 
        """
        return self.city.strip().lower() in value_default
    
    def produce_check_kyiv_active(self) -> bool:
        """
        Method which is dedicated to check the values of the 
        Input:  None
        Output: we developed the check of the active
        """
        #TODO think about it later
        return self.find_element_by_css_selector('div.item.active').text.strip().lower() == Address.city_kyiv

    def produce_search_city(self) -> None:
        """
        Method which is dedicated to search the city values of the selected values
        Input:  None
        Output: we developed the city values
        """
        # self.find_elements_by_css_selector('div.v-input__control')[1].click()
        self.find_element_by_css_selector('input#input-15').click()
        if not self.produce_check_kyiv_development():
            return
        elif self.produce_check_kyiv_development() and not self.produce_check_kyiv_active():
            for f in self.find_elements_by_css_selector('div.item'):
                if f.text.strip() and f.text.strip().lower() == Address.city_kyiv:
                    f.click()
                    break
        return

    def produce_check_active_city(self) -> bool:
        """
        Method which is dedicated to develop the city check
        Input:  value_string = value of the selected string for getting
        Output: we developed the check of the selected current value
        """
        # item active
        pass

    def produce_search_rooms(self, value_element:str) -> None:
        """
        Method which is dedicated to add search rooms button
        Input:  None
        Output: We added the selected search for the rooms
        """
        self.find_element_by_css_selector('input#txtFilterItem').click()
        for f in self.find_elements_by_css_selector('a[data-group="grpRoomCount"]'):
            if f.text.strip() and f.text == value_element:
                f.click()
                break
            
    def produce_search_district(self) -> None:
        """
        Method which is dedicated to search the district values
        Input:  None
        Output: we put the click on this button
        """
        for f in self.find_elements_by_css_selector('label.list-item--label'):
            if f.text and f.text.strip().lower() == self.district:
                f.click()
                break
        self.find_element_by_css_selector('div.btn.btn-main').click()

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to add the search price value for the text
        Input:  None
        Output: we developed the values of the price search
        """
        self.find_element_by_css_selector('input#txtPrice').click()
        for f in self.find_elements_by_css_selector('a[data-group="grpPriceNat"]'):
            if f.text.strip() and f.text == self.price:
                print(self.price)
                f.click()
                break

    def produce_search_price_manually(self) -> None:
        """
        Method which is dedicated to add the manual price of it
        Input:  None
        Output: we manually developed values of the price search in manual
        """
        self.find_element_by_css_selector('input#txtPrice').click()
        insert = self.find_element_by_css_selector('input#PriceTo')
        insert.click()
        insert.send_keys(self.price)
        insert.click()
        insert.send_keys(Keys.ENTER)
        
    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to add the search results button
        Input:  None
        Output: we developed click to give search values for it
        """
        self.find_element_by_css_selector('button.btn.btn-main').click()

    def produce_search_result_click_send(self) -> None:
        """
        Method which is dedicated to add the search results button of the sending values
        Input:  None
        Output: we developed click to give search values for it
        """
        self.find_element_by_css_selector('input.send.btn-main').click()

    def produce_search_square_floor(self) -> set:
        """
        Method which is dedicated to develop the lists of square and floor values
        Input:  None
        Output: list of the squares and list of the floors
        """
        value_list_used = [f.text for f in self.find_elements_by_css_selector('div.label')]
        value_square = [f[0] for f in self.produce_chunks(value_list_used, 6)]
        value_floor = [f[4] for f in self.produce_chunks(value_list_used, 6)]
        return value_square, value_floor

    def produce_check_further(self) -> bool:
        """
        Method which is dedicated to work with the values of the next pages
        Input:  None
        Output: we developed the value to check
        """
        value_next = self.find_elements_by_css_selector('a.pagination__arrow')
        if not value_next:
            return False
        value_next = value_next[-1].get_attribute('href')
        if not value_next:
            return False
        return value_next

    def produce_search_results(self) -> None:
        """
        Method which is dedicated to return the basic results to it
        Input:  None
        Output: we developed the full dataframe for all of it
        """
        self.get(Address.link_start)
        
        self.produce_rent_status()
        self.produce_log(Message.message_status_rent)

        if self.city:
            self.produce_search_city()
            if self.district:
                self.produce_search_district()
                self.produce_log(Message.message_district)
        self.produce_search_result_click()
        self.produce_log(Message.message_click)
        
        if self.price_bool and self.price_click:
                self.produce_search_price()
                self.produce_log(Message.message_price)
        elif self.price_bool and not self.price_click:
            self.produce_search_price_manually()
            self.produce_log(Message.message_price)

        value_adress = []
        value_links = []
        value_dates = []
        value_prices = []
        value_desc = []
        value_rooms = []
        value_squares = []
        value_floors = []

        self.produce_log(Message.message_finish_settings)
        if self.rooms:
            for room in self.rooms:
                self.produce_search_rooms(room)
                self.produce_search_result_click_send()
                time.sleep(Address.time_sleep)

                adress = [f.text for f in self.find_elements_by_css_selector('a.link-item')]
                links = [f.get_attribute('href') for f in self.find_elements_by_css_selector('a.link-item')]
                dates = [f.text for f in self.find_elements_by_css_selector('div.last-edit')]
                prices = [f.text for f in self.find_elements_by_css_selector('p.full-price.label')]
                desc = [f.text for f in self.find_elements_by_css_selector('p.text')]
                rooms = [room for _ in links]
                square, floor = self.produce_search_square_floor()
                
                value_use = self.produce_check_further()
                while value_use:
                    self.get(value_use)
                    time.sleep(Address.time_sleep)
                    adress.extend([f.text for f in self.find_elements_by_css_selector('a.link-item')])
                    links.extend([f.get_attribute('href') for f in self.find_elements_by_css_selector('a.link-item')])
                    dates.extend([f.text for f in self.find_elements_by_css_selector('div.last-edit')])
                    prices.extend([f.text for f in self.find_elements_by_css_selector('p.full-price.label')])
                    desc.extend([f.text for f in self.find_elements_by_css_selector('p.text')])
                    rooms = [room for _ in links]

                    square_new, floor_new = self.produce_search_square_floor()
                    square.extend(square_new)
                    floor.extend(floor_new)
                    value_use = self.produce_check_further()
                
                value_adress.extend(adress)
                value_links.extend(links)
                value_dates.extend(dates)
                value_prices.extend(prices)
                value_desc.extend(desc)
                value_rooms.extend(rooms)
                value_squares.extend(square)
                value_floors.extend(floor)
        else:
            self.produce_search_result_click_send()
            value_adress = [f.text for f in self.find_elements_by_css_selector('a.link-item')]
            value_links = [f.get_attribute('href') for f in self.find_elements_by_css_selector('a.link-item')]
            value_dates = [f.text for f in self.find_elements_by_css_selector('div.last-edit')]
            value_prices = [f.text for f in self.find_elements_by_css_selector('p.full-price.label')]
            value_desc = [f.text for f in self.find_elements_by_css_selector('p.text')]
            value_rooms = [room for _ in links]
            value_squares, value_floors = self.produce_search_square_floor()
            
            value_use = self.produce_check_further()
            value_ind = 1
            while value_use:
                self.get(value_use)
                time.sleep(Address.time_sleep)
                value_ind += 1
                self.produce_log(f'We found the other variations, check the {value_ind} page')
                value_adress.extend([f.text for f in self.find_elements_by_css_selector('a.link-item')])
                value_links.extend([f.get_attribute('href') for f in self.find_elements_by_css_selector('a.link-item')])
                value_dates.extend([f.text for f in self.find_elements_by_css_selector('div.last-edit')])
                value_prices.extend([f.text for f in self.find_elements_by_css_selector('p.full-price.label')])
                value_desc.extend([f.text for f in self.find_elements_by_css_selector('p.text')])
                value_rooms = [room for _ in links]
                square_new, floor_new = self.produce_search_square_floor()
                value_squares.extend(square_new)
                value_floors.extend(floor_new)
                value_use = self.produce_check_further()

        self.produce_log(Message.message_done)
        print(
            len(value_adress),
            len(value_links),
            len(value_dates),
            len(value_prices),
            len(value_desc),
            len(value_rooms),
            len(value_squares),
            len(value_floors)
        )
        self.produce_log(Message.message_done_tr)