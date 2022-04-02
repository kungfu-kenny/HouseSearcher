import os
import json
from utilities.work_directories import (
    create_directory, 
    check_presence_file,
    check_presence_directory
)
from config import (
    Lang,  
    Folders,
    Default,
    DefaultDict
)


class StringBasicTransform:
    """
    class which is dedicated to work with the transform value
    """
    def __init__(
        self, 
        lang:str=Lang.ukr, 
        city:str=Default.city_ukr, 
        insert:str=Default.insert, 
        district:str=Default.district,
        rooms:list=Default.rooms,
        price:int=Default.price
    ) -> None:
        self.lang = lang if lang in [Lang.ukr, Lang.rus] else Lang.ukr
        self.city = city
        self.insert = insert
        self.district = district.lower()
        self.rooms = self.get_check_list_number(rooms)
        self.price = self.get_check_number(price)
        self.folder_base = os.path.join(Folders.folder_main, Folders.folder_storage)
        self.folder_json = os.path.join(self.folder_base, Folders.folder_json)
        self.file_json = os.path.join(self.folder_json, Folders.file_json)
        self.file_data = os.path.join(self.folder_json, Folders.file_default_data)

    @staticmethod
    def develop_folder(folder:str) -> None:
        """
        Static method which is dedicated to create basic folders
        Input:  folder = folder used
        Output: we created folders if had to
        """
        if check_presence_directory(folder):
            create_directory(folder)

    def develop_json_values(self) -> None:
        """
        Method which is dedicated to develop the json values of the 
        Input:  None
        Output: we developed the json values for all of it
        """
        self.develop_folder(self.folder_base) or self.develop_folder(self.folder_json)
        if check_presence_file(self.file_json):
            return
        with open(self.file_json, 'w') as file_json:
            json.dump(
                {
                    Lang.ukr:{
                        'city': DefaultDict.value_city_rus_ukr,
                        'district': DefaultDict.value_district_rus_ukr
                    },
                    Lang.rus:{
                        'city': DefaultDict.value_city_ukr_rus,
                        'district': DefaultDict.value_district_ukr_rus
                    }, 
                },
                file_json
            )

    @staticmethod
    def get_check_number(value_input) -> int:
        """
        Static method which is dedicated to check the number of the selected
        Input:  value_input = input which is used values
        Output: int value of the selected number
        """
        if isinstance(value_input, (float, int)):
            return int(value_input)
        try:
            value_input = int(value_input)
            return value_input
        except Exception:
            return 0

    @classmethod
    def get_check_list_number(cls, value_list:list) -> list:
        """
        Class method which is dedicated to check the values of the
        Input:  value_list = list of the used 
        Output: list values which could be used for the rooms
        """
        if value_list:
            value_list = [cls.get_check_number(f) for f in value_list]
            value_list = [f for f in value_list if f]
            return value_list
        return []

    def develop_default_data(self) -> None:
        """
        Method which is dedicated to get random data from the 
        Input:  None
        Output: we created json for getting them as default
        """
        self.develop_folder(self.folder_base) or self.develop_folder(self.folder_json)
        if check_presence_file(self.file_data):
            return
        with open(self.file_data, 'w') as file_json:
            json.dump(
                {
                    Lang.ukr:{
                        "city": Default.city_ukr,
                        "district": "оболонський",
                        "insert": "мінська",
                        "price":23000,
                        "rooms": [2, 3],
                    },
                    Lang.rus:{
                        "city": Default.city_rus,
                        "district": 'оболонский',
                        "insert": "минская",
                        "price":23000,
                        "rooms": [2, 3],
                    }
                },
                file_json
            )

    def get_default_data(self, lang:str=Lang.ukr) -> dict:
        """
        Method which is dedicated to get default data from the json
        Input:  lang = language of the data
        Output: we developed default data for getting them
        """
        self.develop_default_data()
        with open(self.file_data, 'r') as file_json:
            value_dict = json.load(file_json)
        lang = lang if lang in [Lang.ukr, Lang.rus] else Lang.ukr
        return {
            "city": value_dict.get(lang, {}).get("city", Default.city_ukr),
            "rooms": value_dict.get(lang, {}).get('rooms', Default.rooms),
            "price": value_dict.get(lang, {}).get('price', Default.price),
            "insert": value_dict.get(lang, {}).get('insert', Default.insert),
            "district": value_dict.get(lang, {}).get('district', Default.district),
        }

    def main(self) -> set:
        """
        Main method which is dedicated to develop the input values at every case
        Input:  None
        Output: we developed the basic values of the development 
        """
        self.develop_json_values()
        with open(self.file_json, 'r') as file_json:
            value_dict = json.load(file_json)
        city = value_dict.get(self.lang, {}).get('city', {}).get(self.city, Default.city_ukr)
        district = value_dict.get(self.lang, {}).get('district', {}).get(self.district, Default.district)
        return city, self.insert, district, self.rooms, self.price