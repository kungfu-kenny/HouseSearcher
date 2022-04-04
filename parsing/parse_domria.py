from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from utilities.work_dataframes_domria import DevelopDomria
from utilities.work_lists import make_check_list_length
from config import WebDomria, Message


class ParseDomria(ParseMain):
    """
    class which is dedicated to parse the domria website and return selected values
    """
    def __init__(self, driver_path: str, city:str='', insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseDomria, self).__init__(driver_path)
        self.city = city.capitalize()
        self.used_db = WebDomria.name
        self.web = WebDomria.link_start
        self.link = WebDomria.link_continue
        self.text = insert.lower().strip()
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
            if f.text == WebDomria.rent_status:
                f.click()
                break

    def produce_selected_text_check(self) -> None:
        """
        Method which is dedicated to return the check of the adequate text
        Input:  None
        Output: we developed the check of the selected text
        """
        try:
            for f in WebDriverWait(self, 5).until(
                    EC.presence_of_all_elements_located(
                        (
                            By.CLASS_NAME, 
                            'item'
                        )
                    )
                ):
                if f.text.lower() == self.text:
                    return True
            return False
        except Exception as e:
            return False

    def produce_selected_text(self) -> None:
        """
        Method which is dedicated to add the selected text and filtrate
        Input:  None
        Output: we added the basic filtration for it
        """
        self.find_element_by_id('autocomplete-1').send_keys(self.text)
        if not self.produce_selected_text_check():
            for _ in self.text:
                self.find_element_by_id('autocomplete-1').send_keys(Keys.BACK_SPACE)
            return
        for f in WebDriverWait(self, 5).until(
                EC.presence_of_all_elements_located(
                    (
                        By.CLASS_NAME, 
                        'item'
                    )
                )
            ):
            if self.text in f.text.lower():
                f.click()
                break

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to add the price status of the search
        Input:  None
        Output: we developed the price filter
        """
        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div#mainAdditionalParams_0'
                )
            )
        )
        
        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div#mainAdditionalParams_0'
                )
            )
        ).click()
        
        after = WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.ID, 
                    '235_to'
                )
            )
        )
        after.send_keys(self.price)
        
        WebDriverWait(self, WebDomria.time_wait).until(
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
        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.ID, 
                    'autocomplete'
                )
            )
        )
        k = self.find_element_by_id('autocomplete')
        k.click()
        k.send_keys(self.city)
        k.send_keys(Keys.ENTER)

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to produce the district of the selected
        Input:  values of the inserted city
        Output: we developed the district searched for the flat
        """
        for types in self.find_elements_by_css_selector('label.tabs-item'):
            if types.text.lower() == self.district.lower():
                types.click()
                break

    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to add filters for the searched rooms
        Input:  None
        Output: we developed the rooms searches
        """
        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div#mainAdditionalParams_1'
                )
            )
        )

        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR, 
                    'div#mainAdditionalParams_1'
                )
            )
        ).click()

        for element in self.find_elements_by_css_selector('label.tabs-item'):
            if element.text:
                if element.text in self.list_rooms:
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
        return \
            WebDriverWait(self, WebDomria.time_wait).until(
                EC.presence_of_element_located(
                    (
                        By.CSS_SELECTOR, 
                        'button.button-border.small.active.noClickEvent'
                    )
                )
            ).text == WebDomria.list_check

    def produce_search_type_markup(self) -> None:
        """
        Method which is dedicated to produce the list values of the filtration
        Input:  None
        Output: we developed the type of the selected markup which would be shown
        """
        for f in WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR, 
                    'button.button-border.small'
                )
            )
        ):
            if f.text == WebDomria.list_check:
                f.click()

    def produce_search_district_text(self) -> None:
        """
        Method which is dedicated to develop the distrinct or text to
        Input:  None
        Output: we clicked on the selected values
        """
        WebDriverWait(self, WebDomria.time_wait).until(
                EC.element_to_be_clickable(
                    (
                        By.CSS_SELECTOR, 
                        'label#geo-box'
                    )
                )
            )
        self.find_element_by_css_selector('input#autocomplete-1').click()
        
    def wait_loading_elements(self, value_wait:str='section.realty-item.isStringView') -> None:
        """
        Method which is dedicated to develop the load waiting for all values
        Input:  value_wait = css selector to wait
        Output: we produced the waiting to the wait of the selected elements
        """
        WebDriverWait(self, WebDomria.time_wait).until(
            EC.presence_of_all_elements_located(
                (
                    By.CSS_SELECTOR,
                    value_wait
                )
            )
        )
        return self.find_elements_by_css_selector(value_wait)

    def produce_check_presence_links(self) -> bool:
        """
        Method which is dedicated to check presence of the links
        Input:  None
        Output: boolean value which checks presence of next values
        """
        if len(self.find_elements_by_css_selector('a.button-border.page-item.next.text-r')) > 0:
            return True
        return False

    def produce_search_click_next(self, value_ind:int=1) -> None:
        """
        Method which is dedicated to click and find next values
        Input:  value_ind = index value which is about to search
        Output: we found the click to the next value
        """
        for f in self.find_elements_by_css_selector('a.button-border'):
            if f.text == str(value_ind):
                self.execute_script("arguments[0].click();", f)
                break

    def produce_search_selected(self, value_used:str, value_searched:str) -> list:
        """
        Method which is dedicated to get values from the search elements
        Input:  value_used = selector where to search
                value_searched = selector of element which is search
        Output: we developed list of the selected values which were searched
        """
        value_return = []
        for f in self.find_elements_by_css_selector(value_used):
            value_check = f.find_elements(By.CSS_SELECTOR, value_searched)
            if value_check:
                value_return.append(value_check[0].text)
            else: value_return.append('')
        return value_return

    def produce_search_results(self, used_results:set) -> None:
        """
        Method which is dedicated to work with the search
        Input:  used_results = set of the datetime and the uuid
        Output: we developed the dataframe of selected values
        """
        self.get(WebDomria.link_start)
        
        #TODO finally check the values of the workplace
        self.produce_rent_status()
        self.produce_log(Message.message_status_rent)
        
        self.produce_search_city_basic()
        self.produce_log(Message.message_city_basic)
        
        self.produce_search_result_click()
        self.produce_log(Message.message_click)
        
        if self.produce_search_type_markup_check():
            self.produce_log(Message.message_markup_success)
        else:
            self.produce_log(Message.message_markup_fail)
            self.produce_search_type_markup()
            self.produce_log(Message.message_markup_change)

        self.produce_search_city()
        self.produce_log(Message.message_city)

        if self.text or self.district:
            self.produce_search_district_text()
            if self.district:
                self.produce_search_district()
                self.produce_log(Message.message_district)
            
            if self.text:
                self.produce_selected_text()
                self.produce_log(Message.message_insert_text)
        
        try:
            if self.price_bool:
                self.produce_search_price()
                self.produce_log(Message.message_price)
            
            if self.list_rooms:
                self.produce_search_rooms()
                self.produce_log(Message.message_rooms)
        except Exception:
            self.produce_log(Message.message_mistake)
        
        self.produce_log(Message.message_finish_settings)
        self.wait_loading_elements()
        
        self.wait_loading_elements('b.size18')
        value_price = [f.text for f in self.wait_loading_elements('b.size18')]
        value_address = [f.text for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')]
        value_address_full = [f.get_attribute('title') for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')]
        value_description = [f.text for f in self.wait_loading_elements('div.mt-15.text.pointer.desc-hidden')]
        value_date = [f.get_attribute('datetime') for f in self.wait_loading_elements('time.size14.flex.mt-10')]
        value_further = [f.text for f in self.wait_loading_elements('div.mt-10.chars.grey')]
        value_links = [f.get_attribute('href') for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')]
        
        value_ind = 1
        while self.produce_check_presence_links():
            value_ind += 1
            self.produce_search_click_next(value_ind)
            self.wait_loading_elements()
            self.produce_log(f'We found the other variations, check the {value_ind} page')
            
            value_price.extend([f.text for f in self.wait_loading_elements('b.size18')])
            value_address.extend([f.text for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')])
            value_address_full.extend([f.get_attribute('title') for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')])
            value_links.extend([f.get_attribute('href') for f in self.wait_loading_elements('a.realty-link.size22.bold.mb-10.break.b')])
            value_description.extend([f.text for f in self.wait_loading_elements('div.mt-15.text.pointer.desc-hidden')])
            value_date.extend([f.get_attribute('datetime') for f in self.wait_loading_elements('time.size14.flex.mt-10')])
            value_further.extend([f.text for f in self.wait_loading_elements('div.mt-10.chars.grey')])

        # print(
        #     len(value_address),
        #     len(value_links), 
        #     len(value_date),
        #     len(value_address_full),
        #     len(value_description),
        #     len(value_date),
        #     len(value_further),
        #     len(value_price)
        # )
        self.produce_log(Message.message_done)
        if make_check_list_length(
            value_address,
            value_links,
            value_date,
            value_price,
            value_description,
            value_further,
            value_address_full
        ):
            transformated = DevelopDomria(
                self.used_db,
                value_address,
                value_links,
                value_date,
                value_price,
                value_description,
                value_further,
                value_address_full,
                self.price,
                self.list_rooms
            ).produce_transform_dataframe(used_results)
        else:
            transformated = DevelopDomria(
                self.used_db,
                value_address,
                value_links,
                value_date,
                value_price,
                value_description,
                value_further,
                value_address_full,
                self.price,
                self.list_rooms
            ).produce_empty()
            self.produce_log(Message.message_empty)
        self.produce_log(Message.message_done_tr)
        return transformated