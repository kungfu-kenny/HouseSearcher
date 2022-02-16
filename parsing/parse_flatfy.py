from pprint import pprint
from tkinter.messagebox import NO
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.work_lists import make_list_sublists, make_list_transpose
from parsing.parse_main import ParseMain
from config import WebFlatfy


class ParseFlatfly(ParseMain):
    """
    class which is dedicated to work with the flatly
    """
    def __init__(self, driver_path: str, list_rooms:list=[], value_price:int=0, text:str='') -> None:
        super(ParseFlatfly, self).__init__(driver_path)
        self.link = '/'.join([WebFlatfy.link_start, WebFlatfy.link_continue])
        self.text = text
        self.price = self.produce_price(value_price)
        self.list_rooms = self.produce_list_rooms(list_rooms)
        
    @staticmethod
    def produce_price(value_price:int) -> str:
        """
        Static method which is dedicated to get value price
        Input:  value_price = int value which was 
        Output: string which is about the 
        """
        if not value_price:
            return 'любая'
        if (isinstance(value_price, int) or isinstance(value_price, float)) and value_price <= 15000:
            return 'до 15 000 грн'
        if (isinstance(value_price, int) or isinstance(value_price, float)) and value_price <= 20000:
            return 'до 20 000 грн'
        if (isinstance(value_price, int) or isinstance(value_price, float)) and value_price <= 40000:
            return 'до 40 000 грн'
        if (isinstance(value_price, int) or isinstance(value_price, float)) and value_price <= 60000:
            return 'до 60 000 грн'
        
    @staticmethod
    def make_adress_check(value_list:list) -> set:
        """
        Function which is dedicated to work with the
        Input:  value_list = list of the given adress
        Output: set with selected lists of the values
        """
        value_full_adresses, value_subdist, value_district, value_city = [], [], [], []
        for value in value_list:
            if len(value) == 4:
                adress, subdist, district, city = value
            elif len(value) == 3:
                value_check, district, city = value
                if 'жк' in value_check.lower() or 'ул.' in value_check.lower():
                    adress = value_check
                    subdist = ''
                else:
                    adress = ''
                    subdist = value_check
            else:
                adress, subdist, district, city = '', '', '', ''
            value_full_adresses.append(adress)
            value_subdist.append(subdist)
            value_district.append(district)
            value_city.append(city)
        return value_full_adresses, value_subdist, value_district, value_city

    @staticmethod
    def produce_list_rooms(list_rooms:list) -> list:
        """
        Static method which is dedicated to work with the lists of rooms
        Input:  list_rooms = list which was given to developed values
        Output: list of developed rooms to find them into the 
        """
        value_return = []
        for list_room in list_rooms:
            if isinstance(list_room, int) or isinstance(list_room, float) and 5 > list_room > 0:
                value_return.append(str(int(list_room)))
            elif isinstance(list_room, int) or isinstance(list_room, float) and list_room > 4:
                value_return.append('5+')
        return value_return

    def get_value_bool(self) -> bool:
        """
        Method which is dedicated to return bool value for the
        Input:  None
        Output: boolean values which were dedicated to get it
        """
        return len(
            self.find_elements_by_css_selector(
                'a.paging-nav--right.paging-button.paging-nav')) > 0

    def produce_rooms_number(self) -> None:
        """
        Method which is dedicated to produce the rooms numbers to it
        Input:  None
        Output: we developed values of the rooms
        """
        WebDriverWait(self, WebFlatfy.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    "button#menu-trigger-room_count"
                    )
                )
            ).click()
        
        value_list = self.find_element_by_css_selector(
            'div.mui-list.mui-list--padding.menu-list')
        value_check = value_list.find_elements(
            By.CSS_SELECTOR, 
            'span.select-multiple__item-inner')
        value_click = value_list.find_elements(
            By.CSS_SELECTOR, 
            'canvas.button-base__ripple')
        
        value_select = False
        for v, c in zip(value_check, value_click):
            if v.text in self.list_rooms:    
                c.click()
                if not value_select: value_select = True 
        
        if value_select:
            v = self.find_element_by_css_selector(
                'button.button-base.button-common.button-common--variant-text.'\
                'button-common--size-small.button-common--primary.button-common--full-width')
            v.find_element(
                By.CSS_SELECTOR, 
                'canvas.button-base__ripple').click()
        
    def produce_price_count(self) -> None:
        """
        Method which is dedicated to work with the giving values
        Input:  given values of the price
        Output: None
        """
        WebDriverWait(self, WebFlatfy.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    "button#menu-trigger-price"
                    )
                )
            ).click()
        
        value_check = self.find_element_by_css_selector('div#menu-price')
        value_drop_price = value_check.find_element(By.CSS_SELECTOR, 'div.mui-list.mui-list--padding.menu-list')
        ind = [f.text for f in value_drop_price.find_elements(
            By.CSS_SELECTOR, 
            'div.button-base.mui-list-item.mui-list-item--button.menu-list__item.menu-list__item--button')
            ].index(self.price)
        value_drop_price.find_elements(By.TAG_NAME, 'canvas')[ind].click()#.button-base__ripple')

    def produce_selected_text(self) -> None:
        """
        Method which is dedicated to give the selected input of the text
        Input:  None
        Output: None
        """
        if self.text:
            input_text = self.find_element_by_id('downshift-0-input')
            input_text.send_keys(self.text)
            # button_press = self.find_elements_by_css_selector(
            #     'div.button-base.mui-list-item.mui-list-item--button.menu-list__item.menu-list__item--button')[-1]
            button_press = WebDriverWait(self, WebFlatfy.time_wait).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR, 
                        'div.button-base.mui-list-item.mui-list-item--button.menu-list__item.menu-list__item--button'
                        )
                    )
                )[-1]
            WebDriverWait(button_press, WebFlatfy.time_wait).until(
                EC.presence_of_element_located(
                    (
                        By.TAG_NAME, 
                        'canvas'
                        )
                    )
                ).click()
            # button_press.find_element(By.TAG_NAME, 'canvas').click()
            # input_text.submit()

    def produce_searched_links(self) -> list:
        """
        Method which is dedicated to return searched links
        Input: None
        Output: list of desired links
        """
        self.wait_loading_elements('a.realty-preview-title__link')
        return  [
            f.get_attribute('href') for f in self.find_elements_by_css_selector(
                'a.realty-preview-title__link'
            )
        ]#[::2]

    def produce_searched_prices(self) -> list:
        """
        Method which is dedicated to return searched prices
        Input:  None
        Output: list of the selected prices
        """
        self.wait_loading_elements('div.realty-preview-price.realty-preview-price--main')
        return [
            f.text for f in self.find_elements_by_css_selector(
                'div.realty-preview-price.realty-preview-price--main')]

    def produce_searched_prices_sqr(self) -> list:
        """
        Method which is dedicated to return searched prices square
        Input:  None
        Output: list of the prices square
        """
        self.wait_loading_elements('div.realty-preview-price.realty-preview-price--sqm')
        return [
            f.text for f in self.find_elements_by_css_selector(
                'div.realty-preview-price.realty-preview-price--sqm')]

    def produce_searched_street_basic(self) -> list:
        """
        Method which is dedicated to return street basic
        Input:  None
        Output: list with the links
        """
        self.wait_loading_elements('h3.realty-preview-title')
        return [
            f.text for f in self.find_elements_by_css_selector('h3.realty-preview-title')]

    def wait_loading_elements(self, value_base:str='div.feed-layout__item-holder') -> None:
        """
        Method which is dedicated to wait elements to load
        Input:  value_base = multiple selector to wait
        Output: None
        """
        # self.implicitly_wait(5)
        WebDriverWait(self, WebFlatfy.time_wait).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR, 
                    value_base
                    )
                )
            )

    def produce_searched_description(self) -> list:
        """
        Method which is dedicated to work with the values
        Input:  None
        Output: list of descriptions about the flats
        """
        self.wait_loading_elements('p.realty-preview-description__text')
        return [
            f.text for f in self.find_elements_by_css_selector('p.realty-preview-description__text')]
        
    def produce_search_results(self):
        """
        Method which is dedicated for the testing of the selected values
        Input:  None
        Output: we developed values
        """
        self.get(self.link)
        
        self.produce_rooms_number()
        self.produce_price_count()
        self.produce_selected_text()
        
        self.wait_loading_elements()
        print('The characteristics were set')
        
        value_links = self.produce_searched_links()
        value_prices = self.produce_searched_prices()
        value_prices_sqr = self.produce_searched_prices_sqr()
        value_streets_basic = self.produce_searched_street_basic()
        value_descriptions = self.produce_searched_description()
        
        self.wait_loading_elements('div.realty-preview-sub-title-wrapper')
        value_full_adresses, value_subdists, value_districts, value_cities = \
            self.make_adress_check(
                [
                    [k.text for k in f.find_elements(By.TAG_NAME, 'a')] 
                    for f in self.find_elements_by_css_selector('div.realty-preview-sub-title-wrapper')
                    ]
                )
        
        self.wait_loading_elements('div.realty-preview-properties-item')
        value_rooms, value_squares, value_floors, value_types, value_repairs, value_years = \
            make_list_transpose(
                make_list_sublists(
                    [f.text for f in self.find_elements_by_css_selector(
                        'div.realty-preview-properties-item')
                    ], 
                    6)
                )
        value_ind = 1
        while self.get_value_bool():
            value_ind += 1
            print(f'We found the other variations, check the {value_ind} page')
            
            # self.implicitly_wait(5)
            WebDriverWait(self, WebFlatfy.time_wait).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR, 
                        'a.paging-nav--right.paging-button.paging-nav'
                        )
                    )
                ).click()
            # self.find_element_by_css_selector('a.paging-nav--right.paging-button.paging-nav').click()
            
            self.wait_loading_elements()

            value_links.extend(self.produce_searched_links())
            value_prices.extend(self.produce_searched_prices())
            value_prices_sqr.extend(self.produce_searched_prices_sqr())
            value_streets_basic.extend(self.produce_searched_street_basic())
            value_descriptions.extend(self.produce_searched_description())

            self.wait_loading_elements('div.realty-preview-sub-title-wrapper')
            value_full_adress, value_subdist, value_district, value_city = \
                self.make_adress_check(
                    [
                        [k.text for k in f.find_elements(By.TAG_NAME, 'a')] 
                        for f in self.find_elements_by_css_selector('div.realty-preview-sub-title-wrapper')
                        ]
                    )
            value_full_adresses.extend(value_full_adress)
            value_subdists.extend(value_subdist)
            value_districts.extend(value_district)
            value_cities.extend(value_city)

            self.wait_loading_elements('div.realty-preview-properties-item')
            value_room, value_square, value_floor, value_type, value_repair, value_year = \
                make_list_transpose(
                    make_list_sublists(
                        [f.text for f in self.find_elements_by_css_selector(
                            'div.realty-preview-properties-item')
                        ], 
                        6)
                    )
            value_rooms.extend(value_room) 
            value_squares.extend(value_square)
            value_floors.extend(value_floor)
            value_types.extend(value_type) 
            value_repairs.extend(value_repair) 
            value_years.extend(value_year)

        # print('Links', len(value_links))
        # print('Prices', len(value_prices))
        # print('Prices Sqr', len(value_prices_sqr))
        # print('Streets Base', len(value_streets_basic))
        # print('Descriptions', len(value_descriptions))
        # print('Full addr', len(value_full_adresses))
        # print('Sub dists', len(value_subdists))
        # print('Cities', len(value_cities))
        # print('Rooms', len(value_rooms))
        # print('Square', len(value_squares))
        # print('Floors', len(value_floors))
        # print('Types', len(value_types))
        # print('Repairs', len(value_repairs))
        # print('Years', len(value_years))