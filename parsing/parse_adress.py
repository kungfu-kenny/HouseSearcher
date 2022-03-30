import time
from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain
from config import Message


class ParseAdress(ParseMain):
    """
    class which is dedicated to develop the parsing of the adress
    """
    def __init__(self, driver_path:str, insert:str='', district:str='', rooms:list=[], price:int=0) -> None:
        super(ParseAdress, self).__init__(driver_path)
        self.city = 'киев'

    @staticmethod
    def produce_list_rooms(rooms:list) -> list:
        """
        Static method which is dedicated to get the list of rooms
        Input:  rooms = list of the rooms to use
        Output: list of the rooms to use
        """
        return [str[room] for room in rooms]

    def produce_rent_status(self) -> None:
        """
        Method which is dedicated to develop the rent status for it
        Input:  None
        Output: we developed the rent status for change
        """
        if self.find_element_by_css_selector('li.tab.pointer.active').text == 'Снять':
            return
        for element in self.find_elements_by_css_selector('li.tab.pointer'):
            if element.text.strip() == 'Снять':
                element.click()
                break
    
    def produce_check_kyiv_development(self) -> bool:
        """
        Method which is dedicated to check that it is kyiv developed
        Input:  None
        Output: boolean value which is about check that we are using the kyiv 
        """
        return self.city.strip().lower() == 'киев'

    def produce_search_city(self) -> None:
        """
        Method which is dedicated to search the city values of the selected values
        Input:  None
        Output: we developed the city values
        """
        self.find_element_by_id('input-15').click()
        #TODO add here the system about the houses

    def produce_check_active_city(self) -> bool:
        """
        Method which is dedicated to develop the city check
        Input:  value_string = value of the selected string for getting
        Output: we developed the check of the selected current value
        """
        # item active
        pass

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to search the district values
        Input:  None
        Output: we put the click on this button
        """
        pass

    def produce_search_results(self) -> None:
        """
        Method which is dedicated to return the basic results to it
        Input:  None
        Output: we developed the full dataframe for all of it
        """
        self.get('https://address.ua')
        self.produce_rent_status()
        # time.sleep(2)
        self.produce_search_city()
        # time.sleep(2)