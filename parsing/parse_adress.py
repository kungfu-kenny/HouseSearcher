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


    def produce_search_results(self) -> None:
        """
        
        """
        pass