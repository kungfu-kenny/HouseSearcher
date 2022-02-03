from pydoc import cli
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
        
from parsing.parse_main import ParseMain
from config import WebOlx


class ParseOlx(ParseMain):
    """
    class which is dedicated to produce_values of the olx website
    """
    def __init__(self, path_driver:str, text_insert:str='', text_district:str='', list_rooms:list=[]) -> None:
        super(ParseOlx, self).__init__(path_driver)
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

    def get_link_values(self, link:str) -> None:
        """
        Method which is dedicated to check values of links
        Input:  link = link where to get these values
        Output: we created values of the html links
        """
        self.get(link)

    def click_search(self) -> None:
        """
        Method which is dedicated to click the search of the given values
        Input:  None
        Output: we started searching the selected values
        """
        click_button = self.find_element_by_css_selector('span.button.search.submit.active')
        print(click_button)
        print('$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$')
        print(click_button.text)
        click_button.click()
        
    def produce_search_district(self) -> None:
        """
        Method which is dedicated to click on the selected district which is going to be searched
        Input:  None
        Output: we developed the values of the getting district
        """
        f = self.find_element_by_css_selector('ul.small.suggestinput.bgfff.lheight20.br-3.abs.districts.binded')
        for k in f.find_elements(By.TAG_NAME,"li"):
            if k.text.lower() == self.text_district.lower():
                self.execute_script(
                    "arguments[0].click();", 
                    k.find_element(
                        By.TAG_NAME,
                        'a'
                        )
                    )
                break

    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to click on required rooms
        Input:  None
        Output: we developed new rooms to the search
        """
        div_check = self.find_element_by_css_selector('li#param_number_of_rooms_string')
        class_check = div_check.find_element(By.TAG_NAME, 'a')
        class_check.click()
        span_check = class_check.find_element(By.CSS_SELECTOR, 'span.header.block')
        span_check.click()
        ul = self.find_element_by_css_selector('ul.small.suggestinput.bgfff.lheight20.br-3.abs.select.binded')
        for li in ul.find_elements(By.TAG_NAME, "li"):
            if li.text in self.list_rooms:
                self.execute_script(
                    "arguments[0].click();", 
                    li.find_element(
                        By.TAG_NAME,
                        'input'
                        )
                    )

    def produce_search_results(self) -> set:
        """
        Method which is dedicated to get values
        Input:  previously developed link
        Output: we developed list with selected values
        """
        self.get(self.link)
        
        click_district = self.find_element_by_css_selector('span.header.block')
        click_district.click()
        ul = self.find_element_by_css_selector('ul.small.suggestinput.bgfff.lheight20.br-3.abs.districts.binded')
        for li in ul.find_elements(By.TAG_NAME,"li"):
            if li.text.lower() == self.text_district.lower():
                self.execute_script(
                    "arguments[0].click();", 
                    li.find_element(
                        By.TAG_NAME,
                        'a'
                        )
                    )
                break
        
        div_check = self.find_element_by_css_selector('li#param_number_of_rooms_string')
        class_check = div_check.find_element(By.TAG_NAME, 'a')
        class_check.click()
        # span_check = class_check.find_element(By.CSS_SELECTOR, 'span.header.block')
        span_check = WebDriverWait(class_check, WebOlx.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'span.header.block'
                    )
                )
            )
        
        span_check.click()
        # ul = self.find_element_by_css_selector('ul.small.suggestinput.bgfff.lheight20.br-3.abs.select.binded')
        ul = WebDriverWait(self, WebOlx.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'ul.small.suggestinput.bgfff.lheight20.br-3.abs.select.binded'
                    )
                )
            )
        for li in ul.find_elements(By.TAG_NAME, "li"):
            if li.text in self.list_rooms:
                self.execute_script(
                    "arguments[0].click();", 
                    li.find_element(
                        By.TAG_NAME,
                        'input'
                        )
                    )
    
        click_button = self.find_element_by_css_selector('span.button.search.submit.active')
        click_button.click()
        # table_flat = table_flat.find_element(By.CSS_SELECTOR, 'table#offers_table.fixed.offers.breakword.redesigned')
        # table_flat = self.find_element_by_css_selector("table#offers_table")
        table_flat = WebDriverWait(self, WebOlx.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    "table#offers_table"
                    )
                )
            )
        print(table_flat)
        print('5555555555555555555555555555555555555555555555555555555555555')
        table_flats = table_flat.find_elements(By.CSS_SELECTOR, "tr.wrap")
        # table_flats = WebDriverWait(
        #     table_flat, WebOlx.time_wait).until(
        #     EC.presence_of_element_located(
        #         (
        #             By.CSS_SELECTOR, 
        #             "tr.wrap"
        #             )
        #         )
        #     )
        value_list = []
        for table in table_flats[:1]:
            print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii')
            value_name = table.find_element(By.TAG_NAME, 'h3').text
            value_price = table.find_element(By.CSS_SELECTOR, 'td.wwnormal.tright.td-price').text
            # value_date = table.find_elements(By.CSS_SELECTOR, "small.breadcrumb.x-normal")
            print('666666666666666666666666666666666666666666666666666666666666666666666')
            # value_link = table.find_element(By.CSS_SELECTOR, 'a.marginright5.link.linkWithHash.detailsLink').href
            value_place = 1
            print(table)
            print(value_name, value_price)
            print(',,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,')
        # print(table_flats)
        # print(flats_values)
        print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')