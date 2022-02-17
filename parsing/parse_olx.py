import requests
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utilities.work_lists import make_list_sublists
from parsing.parse_main import ParseMain
from config import WebOlx


class ParseOlx(ParseMain):
    """
    class which is dedicated to produce_values of the olx website
    """
    def __init__(self, driver_path:str, text_insert:str='', text_district:str='', list_rooms:list=[]) -> None:
        super(ParseOlx, self).__init__(driver_path)
        self.link = self.produce_link(text_insert)
        self.text_district = text_district
        self.list_rooms = self.produce_list_rooms(list_rooms)

    @staticmethod
    def produce_list_rooms(list_rooms:list) -> list:
        """
        Static method which is dedicated 
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
            return f"{WebOlx.link}/q-{text_insert.lower()}/"
        return WebOlx.link

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to make the search by district
        Input:  None
        Output: we developed the 
        """
        WebDriverWait(self, WebOlx.time_wait).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    'span.header.block'
                    )
                )
            ).click()

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
        try:
            self.implicitly_wait(10)
            print('Started checking the rooms')
            WebDriverWait(self, WebOlx.time_wait).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR, 
                        'span.header.block'
                        )
                    ) and
                EC.element_located_to_be_selected(
                    (
                        By.CSS_SELECTOR, 
                        'div.filter-item.rel.filter-item-number_of_rooms_string'
                        )
                    ) and 
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        'div.filter-item.rel.filter-item-number_of_rooms_string'
                        )
                    )
                ).click()
            print('Clicked')
            for li in self.find_element_by_css_selector(
                    'ul.small.suggestinput.bgfff.lheight20.br-3.abs.select.binded'
                    ).find_elements(By.TAG_NAME, "li"):
                if li.text in self.list_rooms:
                    self.execute_script(
                        "arguments[0].click();", 
                        li.find_element(
                            By.TAG_NAME,
                            'input'
                            )
                        )
        except Exception:
            print('We could not set up the room settings')
    
    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to produce the click of the searches
        Input:  None
        Output: we clicked on the search button
        """
        WebDriverWait(self, WebOlx.time_wait).until(
            EC.element_to_be_clickable(
                (
                    By.CSS_SELECTOR, 
                    "input#search-submit"
                    )
                )
            ).click()
        # self.implicitly_wait(10)
        
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

        self.produce_search_district()
        self.produce_search_rooms()
        self.produce_search_result_click()

        WebDriverWait(self, WebOlx.time_wait).until(
            EC.visibility_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    'td.title-cell'
                )
            )
        )
        print('Done the adding values')
        
        prices = [f.text for f in WebDriverWait(self, WebOlx.time_wait
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'p.price'
                    )
                )
            )]
        pprint(prices)
        print('=============================================================')
        names = [f.text for f in WebDriverWait(self, WebOlx.time_wait
            ).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'h3.lheight22.margintop5'
                    )
                )
            )]
        pprint(names)
        print('=============================================================')
        
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
        
        pprint(places)
        print('=============================================================')
        
        pprint(date)
        print('=============================================================')
        
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
        pprint(links)
        print('=============================================================')
        
        value_ind = 2
        value_link = self.check_element_clickable()
        while value_link:
            self.get(value_link)
            print(f'We found the other variations, check the {value_ind} page')
            value_ind += 1
            WebDriverWait(self, WebOlx.time_wait).until(
                EC.visibility_of_all_elements_located(
                    (
                        By.CSS_SELECTOR,
                        'td.title-cell'
                    )
                )
            )
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
        print(len(names), len(places), len(prices), len(links), len(date))
