from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain


class ParseRieltor(ParseMain):
    """
    class which is dedicated to parse the rieltor website
    """
    def __init__(self, driver_path: str, text_insert:str='', text_district:str='', list_rooms:list=[]) -> None:
        super(ParseRieltor, self).__init__(driver_path)

    def develop_city(self) -> None:
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

    def develop_rent(self) -> None:
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

    def develop_search(self) -> None:
        """
        Method which is dedicated to produce the search button click
        Input:  None
        Output: we develop the search button 
        """
        self.find_element_by_css_selector('button.nav_search_btn').click()

    def wait_loading(self, value_element:str="div.catalog-item__info") -> None:
        """
        Method which is dedicated to develop the load of the 
        Input:  value_element = element which is required to wait
        Output: we waited to load elements
        """
        WebDriverWait(self, 5).until(
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

    def produce_search_elements_empty(self) -> list:
        """
        Method which is dedicated to develop the search elements of unneccessary element
        Input:  
        Output: we developed the list of this values
        """
        #TODO wrote here
        pass

    def produce_search_results(self) -> list:
        """
        Method which is dedicated to return values of the results by the flats
        """
        self.get('https://rieltor.ua/flats-rent/')
        
        self.develop_city()
        print('ssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssssss')

        self.develop_rent()
        print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')

        input_text = self.find_element_by_css_selector('input.nav_street_input')
        input_text.click()
        input_text.send_keys('мінська')
        for element, but in zip(
            self.find_elements_by_css_selector('div.nav_item_option_rayon.js_nav_rayon'), 
            self.find_elements_by_css_selector('div.nav_item_rayon_checkbox')):
            if element.text == 'Оболонський':
                but.click()
                break
        print('zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
        
        self.develop_search()
        print('vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv')
        
        self.wait_loading()
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
        streets = [f.text for f in self.find_elements_by_css_selector('div.catalog-item__title_street')]
        pprint(streets)
        print('===============================================================================')
        
        links = [f.find_element(By.TAG_NAME, 'a').get_attribute('href') for f in self.find_elements_by_css_selector('h2.catalog-item__title')]
        pprint(links)
        print('===============================================================================')
        
        districts = [f.text for f in self.find_elements_by_css_selector('div.catalog-item__title_district')]
        pprint(districts)
        print('===============================================================================')
        
        prices = [f.text for f in self.find_elements_by_css_selector('strong.catalog-item__price')]
        pprint(prices)
        print('===============================================================================')
        
        #TODO rewrote as function
        subways = [f.text for f in self.find_elements_by_css_selector('a.label.label_location.label_location_subway')]
        pprint(subways)
        print('===============================================================================')
        
        #TODO rewrote as function
        types = [f.text for f in self.find_elements_by_css_selector('span.label.label_attention')]
        pprint(types)
        print('===============================================================================')
        
        #TODO rewrote as function
        commission = [f.text for f in self.find_elements_by_css_selector('span.label.label_no_commission')]
        pprint(commission)
        print('===============================================================================')
        
        values = [f.text for f in self.find_elements_by_css_selector('div.catalog-item_info-item-row')]
        pprint(values)
        print('===============================================================================')
        
        #TODO rewrote as function
        descriptions = [f.text for f in self.find_elements_by_css_selector('p.catalog-item_info-item-row.catalog-item_info-description')]
        print(descriptions[0])
        print('===============================================================================')

        print(len(streets), len(links), len(districts), len(prices), len(subways), len(types), len(commission), len(values), len(descriptions))
        ind = 1
        value_now = self.develop_values_further(ind)

        #TODO add to the adding to the links
        while value_now:
            self.get(value_now)
            self.wait_loading()
            
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
            
            print(len(streets), len(links), len(districts), len(prices))
            print('===============================================================================')
            
            ind += 1
            value_now = self.develop_values_further(ind)
            