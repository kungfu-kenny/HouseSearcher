import os
import re
import zipfile
import requests
from utilities.work_directories import create_directory, check_presence_file
from config import Folders, WebDriver

class ParseWebDriver:
    """
    class which is dedicated to get the webdriver to the selected value
    """
    def __init__(self) -> None:
        self.path_storage = os.path.join(Folders.folder_main, Folders.folder_storage)
        self.path_webdriver_file = os.path.join(self.path_storage, WebDriver.name)
        self.path_webdriver_archive = os.path.join(self.path_storage, WebDriver.name_archive)
        
    def check_webdriver_status(self) -> int:
        """
        Method which is dedicated to use all that we have and return the number of the scenario
        Input:  All what we have previously
        Output: int value which shows what we need to do after
        """
        presence_archive = check_presence_file(self.path_webdriver_archive)
        presence_file = check_presence_file(self.path_webdriver_file)
        if presence_file:
            return 1
        if presence_archive:
            return 2
        return 0

    def download_webdriver(self) -> None:
        """
        Method which is dedicated to download webdriver
        """
        archive_value = requests.get(WebDriver.link, stream=True)
        with open(self.path_webdriver_archive, 'wb') as archive_new:
            archive_new.write(archive_value.content)

    def extract_webdriver(self) -> None:
        """
        Method which is dedicated to extract webdriver
        """
        with zipfile.ZipFile(self.path_webdriver_archive) as myzip:
            if 'chromedriver' in myzip.namelist():
                myzip.extract('chromedriver', self.path_storage)
                os.chmod(os.path.join(self.path_storage, 'chromedriver'), 755)

    def remove_archive(self) -> None:
        """
        Method which is dedicated to remove archives to all of it
        """
        os.path.exists(self.path_webdriver_archive) and os.remove(self.path_webdriver_archive)

    def check_webdriver_main(self) -> str:
        """
        Main method which fully automates the process of getting the webdriver for all of it
        Input:  All previous values
        Output: path to the webdriver
        """
        create_directory(self.path_storage)
        scenario = self.check_webdriver_status()
        if scenario in [0]:
            self.download_webdriver()
        if scenario in [0, 2]:
            self.extract_webdriver()
        if WebDriver.remove:
            self.remove_archive()
        return self.path_webdriver_file