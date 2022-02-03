from selenium import webdriver
from selenium.webdriver import Chrome, ChromeOptions
from fake_useragent import UserAgent


class ParseMain(Chrome):
    """
    Class for the getting values from all of it
    """
    def __init__(self, driver_path:str) -> None:
        super(ParseMain, self).__init__(
            executable_path=driver_path, 
            chrome_options=self.get_credentials()
            )

    def get_credentials(self) -> object:
        """
        Method which is dedicated to return some credentials for all of this cases
        Input:  All previously given values
        Output: 
        """
        options = ChromeOptions()
        # options.add_argument("headless")
        options.add_argument(f"user-agent={UserAgent().random}")
        return options