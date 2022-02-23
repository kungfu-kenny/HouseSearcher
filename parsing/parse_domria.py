from pprint import pprint
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsing.parse_main import ParseMain


class ParseDomria(ParseMain):
    """
    class which is dedicated to parse the domria website and return selected values
    """
    def __init__(self, driver_path: str) -> None:
        super(ParseMain, self).__init__(driver_path)