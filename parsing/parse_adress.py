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

    @staticmethod
    def produce_list_rooms(rooms:list) -> list:
        """
        Static method which is dedicated to get the list of rooms
        Input:  rooms = list of the rooms to use
        Output: list of the rooms to use
        """
        return [str[room] for room in rooms]

    def produce_search_results(self) -> None:
        """
        Method which is dedicated to return the basic results to it
        Input:  None
        Output: we developed the full dataframe for all of it
        """
        pass