import os
from pprint import pprint
import pandas as pd
from utilities.work_directories import (
    create_directory, 
    check_presence_file, 
    check_presence_directory
)
from config import Folders#, Columns


class DevelopResults:
    """
    class which is dedicated to develop the output of the parsed values
    """
    def __init__(self) -> None:
        self.folder_storage = os.path.join(Folders.folder_main, Folders.folder_storage)
        self.folder_results = os.path.join(self.folder_storage, Folders.folder_results)
    
    @classmethod
    def produce_square(cls, squares:list) -> list:
        """
        Static method which is dedicated to develop squares
        Input:  squares = list of squares
        Output: list of new squares
        """
        pass

    @classmethod
    def produce_date(cls, dates:list) -> list:
        """
        Class method which is dedicated to develop datetimes
        Input:  dates = list of dates
        Output: we developed list of the datetimes list
        """
        pass

    @classmethod
    def produce_price(cls, prices:list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        pass

    @classmethod
    def produce_price_square(cls, prices_sqr:list) -> list:
        """
        Class method which is dedicated to develop prices of the square
        Input:  prices_sqr = list of square prices
        Output: list of new prices
        """
        pass

    @classmethod
    def produce_floor(cls, floors:list) -> list:
        """
        Class method which is dedicated to develop floors
        Input:  floors = list of the floors
        Ouptut: list of the new floor
        """
        pass

    @classmethod
    def produce_room(cls, rooms:list) -> list:
        """
        Class method which is dedicated to develop room answer
        Input:  rooms = list of the parsed rooms
        Output: list of the selected values
        """
        pass 
    
    @staticmethod
    def produce_number(value:str, replacements:list) -> int:
        """
        Static method to work with the numbers
        Input:  value = value which is required to use it
                replacements = value to replcae
        Output: integer value of the number
        """
        for replacement in replacements:
            value = value.replace(replacement, '')
        try:
            return int(value.strip())
        except Exception:
            return -1

    @staticmethod
    def check_folder(folder:str) -> None:
        """
        Static method which is dedicated to check folder 
        Input:  folder = folder to check & create them
        Output: we created folder if it 
        """
        if check_presence_directory(folder):
            create_directory(folder)

    def check_values_presence_folder(self) -> None:
        """
        Method which is dedicated to check presencse of the selected previous
        Input:  None
        Output: we checked selected folders to them
        """
        self.check_folder(self.folder_storage) or self.check_folder(self.folder_results)

    @staticmethod
    def create_dataframe(df:pd.DataFrame, df_path:str) -> None:
        """
        Static method which is dedicated to create dataframe
        Input:  df = pandas DataFrame to save
        Output: we created dataframe if it is necessary
        """
        df.to_csv(df_path, index=False)
    
    @staticmethod
    def create_dataframe_name(path:str, name:str, used:set) -> str:
        """
        Static method which is dedicated to create the name 
        Input:  path = selected path of the dataframe
                name = name of the selected dataframe
                used = set of the unique parameters
        Output: string values of it
        """
        time, uuid = used
        return os.path.join(path, f"{name}_{time}_{uuid}.csv")

    def produce_merge_dataframe(self, dataframes:list) -> pd.DataFrame:
        """
        Method which is dedicated to merge selected dataframes 
        Input:  dataframes = list of the selected dataframes
        Output: we merged dataframes into one
        """
        return pd.concat(dataframes)

    def produce_result(self, dataframes:list, used_results:set) -> pd.DataFrame:
        """
        Method which is dedicated to produce results of every usage
        Input:  dataframes = list of the selected dataframes
                used_results = set of the getting unique data
        Output: we created fully merged dataframe value
        """
        self.check_values_presence_folder()
        dataframe_merge = self.produce_merge_dataframe(dataframes)
        dataframe_name = self.create_dataframe_name(self.folder_results, 'result', used_results)
        if not check_presence_file(dataframe_name):
            self.create_dataframe(dataframe_merge, dataframe_name)
        return dataframe_merge
