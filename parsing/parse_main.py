import os
import logging
from datetime import datetime
# from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from fake_useragent import UserAgent
from utilities.work_directories import create_directory
from config import Folders


class ParseMain(Chrome):
    """
    Class for the getting values from all of it
    """
    def __init__(self, driver_path:str) -> None:
        self.used_db = 'Main'
        self.web = 'None'
        self.folder_logs = os.path.join(
            Folders.folder_main, 
            Folders.folder_logs)
        create_directory(self.folder_logs)
        super(ParseMain, self).__init__(
            executable_path=driver_path, 
            chrome_options=self.get_credentials()
            )
   
    def produce_basic_logs_writing(self, value_message:str) -> None:
        """
        Method which is dedicated to develop the blog
        Input:  value_message = message which is used
        Output: we printed the log to it
        """
        logging.basicConfig(
            filename=os.path.join(self.folder_logs, self.get_date(2)), 
            format='%(message)s', 
            level=logging.INFO
        )
        logging.info(value_message)

    @classmethod
    def get_date(cls, types:int=1) -> str:
        """
        Classmethod which is dedicated to work with a datetime
        Input:  types = type which we require value
        Output: we developed the date
        """
        if types == 1:
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if types == 2:
            return f'{datetime.now().strftime("%Y-%m-%d")}.log'

    def produce_log(self, value_message:str) -> None:
        """
        Method which is dedicated to produce the log of the 
        Input:  
        """
        value_use = f"{self.get_date(1)} | {self.used_db} | {self.web} | {value_message}"
        print(value_use)
        self.produce_basic_logs_writing(value_use)

    def get_credentials(self) -> object:
        """
        Method which is dedicated to return some credentials for all of this cases
        Input:  All previously given values
        Output: 
        """
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        # options.add_argument("headless")
        options.add_argument(f"user-agent={UserAgent().random}")
        return options

    def produce_search_results(self) -> None:
        """
        Method which is dedicated to work with the search results
        Input:  None
        Output: we developed the results of searching to it
        """
        pass

    def produce_search_district(self) -> None:
        """
        Method which is dedicated to make the district search possible
        Input:  None
        Output: we developed the district search which was required
        """
        pass

    def produce_rent_status(self) -> None:
        """
        Method which is dedicated to make filtration by the rent
        Input:  None
        Output: we developed the rent
        """
        pass

    def produce_search_city(self) -> None:
        """
        Method which is dedicated to search the selected city filtration
        Input:  None
        Output: we developed filtration by the city
        """
        pass

    def produce_search_rooms(self) -> None:
        """
        Method which is dedicated to produce the rooms filter
        Input:  None
        Output: we developed filtration of the room number
        """
        pass

    def produce_search_price(self) -> None:
        """
        Method which is dedicated to produce the price filter
        Input:  None
        Output: we developed filtration of the price
        """
        pass

    def produce_search_result_click(self) -> None:
        """
        Method which is dedicated to make the click to find results
        Input:  None
        Output: we got values to search
        """
        pass

    def produce_selected_text(self) -> None:
        """
        Method which is dedicated to make the filtration by inserting text
        Input:  None
        Output: we got inserted the text to filtrate values
        """
        pass

    def wait_loading_elements(self) -> None:
        """
        Method which is dedicated to make the elements loading
        Input:  None
        Output: we developed the load of all elements to grab
        """
        pass

    def produce_price_value(self) -> None:
        """
        Method which is dedicated to created the price value
        Input:  None
        Output: we developed the price value
        """
        pass

    def produce_list_rooms(self) -> list:
        """
        Method which is dedicated to produce list of the rooms
        Input:  None
        Output: produced the list of the selected rooms
        """
        pass