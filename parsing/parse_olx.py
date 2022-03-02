import requests
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.work_lists import make_list_sublists
from parsing.parse_main import ParseMain
from config import WebOlx, Message


class ParseOlx(ParseMain):
    """
    class which is dedicated to produce_values of the olx website
    """
    def __init__(self, driver_path:str, insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseOlx, self).__init__(driver_path)
        self.used_db = WebOlx.name
        self.web = WebOlx.link_start
        self.link = self.produce_link(insert)
        self.text_district = district
        self.list_rooms = self.produce_list_rooms(rooms)
        self.price_bool = bool(price)
        self.price = self.produce_price_value(price)

    @staticmethod
    def produce_price_value(price:int) -> str:
        """
        Static method which is dedicated to produce the selected price of it
        Input:  price = int value of the price to use
        Output: we developed the price to use on them
        """
        if price < 10:
            return '10 грн.'
        if 10 < price <= 100:
            return '100 грн.'
        if 100 < price < 1000:
            return '1 000 грн.'
        if 1000 <= price < 10000:
            return '10 000 грн.'
        if 10000 <= price < 100000:
            return '100 000 грн.'
        if 100000 <= price < 1000000:
            return '1 000 000 грн.'
            
    @staticmethod
    def produce_list_rooms(list_rooms:list) -> list:
        """
        Static method which is dedicated to get values of rooms
        Input:  list_rooms = list of the number rooms
        Output: list of the produce number rooms
        """
        value_list = []
        for room in list_rooms:
            if room == 1:
                value_list.append("1 комната")
            elif 1 < room < 5:
                value_list.append(f'{room} комнаты')
            elif room >= 5:
                value_list.append("5+ комнат")
        return list(set(value_list))

    def produce_link(self, text_insert:str) -> str:
        """
        Method which is dedicated to produce selected link to the 
        Input:  text_insert = inserted values for all of it
        Output: link which would be further parsed
        """
        if text_insert:
            return f"{WebOlx.link_continue}/q-{text_insert.lower()}/"
        return WebOlx.link_continue

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to make the search by district
        Input:  None
        Output: we developed the 
        """
        self.execute_script(
            "arguments[0].click();",
            WebDriverWait(self, WebOlx.time_wait).until(
                EC.element_to_be_clickable(
                    (
                    By.CSS_SELECTOR, 
                    'span.header.block'
                    )
                )
            )
        )

        for li in WebDriverWait(self, WebOlx.time_wait).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    'ul.small.suggestinput.bgfff.lheight20.br-3.abs.districts.binded'
                    )
                )
                ).find_elements(By.TAG_NAME,"li"):
            if li.text.lower() == self.text_district.lower():
                self.execute_script(
                    "arguments[0].click();", 
                    li.find_element(
                        By.TAG_NAME,
                        'a'
                        )
                    )
                break
    
    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to search the room values
        Input:  None
        Output: developed the rooms for the search
        """
        div_search = WebDriverWait(self, WebOlx.time_wait).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        'div.filter-item.rel.filter-item-number_of_rooms_string'
                        )
                    )
                )
        
        self.execute_script(
            "arguments[0].click();",
            WebDriverWait(div_search, WebOlx.time_wait).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        'span.icon.down.abs'
                    )
                )
            )
        )
        for li in self.find_elements_by_css_selector(
            'li.dynamic.clr.brbott-4'
            ):
            if li.text in self.list_rooms:
                self.execute_script(
                    "arguments[0].click();", 
                    li.find_element(
                        By.TAG_NAME,
                        'input'
                        )
                    )

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to produce the price value if the search
        Input:  None
        Output: we created the values
        """
        k = self.find_element_by_css_selector('li#param_price')
        k.find_element(By.CSS_SELECTOR, 'a.button.button-to.numeric.gray.block.fnormal.rel.zi3.clr').click()
        
        for m in WebDriverWait(k, WebOlx.time_wait).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'a.tdnone.block.c27.brbott-4.search-choose'
                )
            )
        ):
            if m.text == self.price:
                m.click()
                break

    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to produce the click of the searches
        Input:  None
        Output: we clicked on the search button
        """
        self.execute_script(
            "arguments[0].click();",
            WebDriverWait(self, WebOlx.time_wait).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        "input#search-submit"
                    )
                )
            )
        )
        
    def wait_loading_elements(self) -> None:
        """
        Method which is dedicated to load all possible elements to grab
        Input:  None
        Output: we develop loading of the elements
        """
        WebDriverWait(self, WebOlx.time_wait).until(
            EC.visibility_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'td.title-cell'
                )
            )
        )

    def check_element_clickable(self) -> bool:
        """
        Method which is dedicated to check next link
        Input:  None
        Output: link which is required to check or the false value
        """
        try:
            a = WebDriverWait(self, WebOlx.time_wait).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        "span.fbold.next.abs.large"
                    )
                )
            )
            link = a.find_element(By.TAG_NAME, 'a').get_attribute('href')
            if 199 < requests.get(link).status_code < 300:
                return link
            return False
        except Exception:
            return False

    def produce_search_results(self) -> set:
        """
        Method which is dedicated to get values
        Input:  previously developed link
        Output: we developed list with selected values
        """
        self.get(self.link)

        if self.list_rooms:
            self.produce_search_rooms()
            self.produce_log(Message.message_rooms)

        if self.price_bool:
            self.produce_search_price()
            self.produce_log(Message.message_price)
            
        if self.text_district:
            self.produce_search_district()
            self.produce_log(Message.message_district)

        self.produce_search_result_click()
        self.produce_log(Message.message_click)

        self.wait_loading_elements()
        
        self.produce_log(Message.message_finish_settings)
        
        prices = [f.text for f in WebDriverWait(self, WebOlx.time_wait
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'p.price'
                    )
                )
            )]
        
        names = [f.text for f in WebDriverWait(self, WebOlx.time_wait
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'h3.lheight22.margintop5'
                    )
                )
            )]
        
        places_all = make_list_sublists(
                [f.text for f in WebDriverWait(self, WebOlx.time_wait
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'small.breadcrumb.x-normal'
                            )
                        )
                    )
                ], 3
            )
        places = [f[1] for f in places_all]
        date = [f[2] for f in places_all]
        
        links = [
            f.get_attribute('href')
            for f in WebDriverWait(self, WebOlx.time_wait
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'a.thumb.vtop.inlblk.rel.tdnone.linkWithHash.scale4.detailsLink'
                    )
                )
            )
        ]
        
        value_ind = 2
        value_link = self.check_element_clickable()
        while value_link:
            self.get(value_link)
            self.produce_log(f'We found the other variations, check the {value_ind} page')
            value_ind += 1

            self.wait_loading_elements()
            
            prices.extend(
                [f.text for f in WebDriverWait(self, WebOlx.time_wait
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'p.price'
                            )
                        )
                    )
                ]
            )
            names.extend(
                [f.text for f in WebDriverWait(self, WebOlx.time_wait
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'h3.lheight22.margintop5'
                            )
                        )
                    )
                ]
            )
            places_all = make_list_sublists(
                [f.text for f in WebDriverWait(self, WebOlx.time_wait
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'small.breadcrumb.x-normal'
                            )
                        )
                    )
                ], 3
            )
            places.extend([f[1] for f in places_all])
            date.extend([f[2] for f in places_all])
            links.extend([f.get_attribute('href')
                for f in WebDriverWait(self, WebOlx.time_wait
                    ).until(
                        EC.presence_of_all_elements_located(
                            (
                                By.CSS_SELECTOR,
                                'a.thumb.vtop.inlblk.rel.tdnone.linkWithHash.scale4.detailsLink'
                            )
                        )
                    )
                ]
            )
            value_link = self.check_element_clickable()
        self.produce_log(Message.message_done)
        
        #TODO add here the first version of transformation
        print(len(names), len(places), len(prices), len(links), len(date))
        self.produce_log(Message.message_done_tr)