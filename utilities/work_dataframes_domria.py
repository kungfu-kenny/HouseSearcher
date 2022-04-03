import os
from pprint import pprint
import pandas as pd
from utilities.work_dataframes import DevelopResults
from config import Columns


class DevelopDomria(DevelopResults):
    """
    class which is dedicated to develop selected dataframes 
    from the Domria calculation
    """
    def __init__(self, name, addresses, links, dates, prices, descs, further, addresses_full, check_price, check_rooms) -> None:
        super(DevelopDomria, self).__init__()
        self.replace_value = 'fgfijogdijgofrdtlcsuzfd;gijolsvkxbczfdsgial;okz'
        self.replace_list = ['кімнати', 'кімната', 'кімнат', 'м²', 'поверх з']
        self.name = name
        self.links = links
        self.dates = dates
        self.descs = descs
        self.addresses_add = addresses_full
        self.check_price = check_price
        self.check_rooms = check_rooms
        self.prices = self.produce_price(prices)
        self.addresses = [self.produce_address_removal(f) for f in addresses]
        self.addresses_name, self.addresses_number = self.produce_address_parse(self.addresses)
        self.rooms, self.squares, self.floors = self.produce_further(further, self.replace_list, self.replace_value)

    @classmethod
    def produce_further(cls, further:list, replace_list:list, replace_value:list) -> list:
        """
        Static method which is dedicated to develop squares
        Input:  squares = list of squares
                replace_list = list which to replace
                replace_value = value to give on the change
        Output: list of new squares
        """
        value_rooms, value_square, value_floor = [], [], []
        for f in further:
            for rep in replace_list:
                f = f.replace(rep, replace_value)
            room, square, floor, *_ = f.split(replace_value)
            value_rooms.append(cls.produce_number(room, [' ']))
            value_square.append(cls.produce_number(square, [' ']))
            value_floor.append(cls.produce_number(floor, [' ']))
        return value_rooms, value_square, value_floor

    @staticmethod
    def produce_address_removal(value_name:str) -> str:
        """
        Static method which is dedicated to removal address types
        Input:  value_name = name where to remove
        Output: 
        """
        for f in ['вул.', 'просп.', 'пров.', 'пр-т', 'наб.']:
            value_name = value_name.replace(f, '')
        return value_name.strip()

    @classmethod
    def produce_address_parse(cls, addresses:list) -> set:
        """
        Class method which is dedicated to work with the
        Input:  adresses = list of the selected values
        Output: we created set of the two values
        """
        address_name, address_number = [], []
        for address in addresses:
            address_split = address.split(', ')
            if len(address_split) == 1:
                address_str = address_split[0]
            else:
                address_str = address_split[0]
                address_int = address_split[-1] 
            address_name.append(address_str.strip())
            address_number.append(address_int.strip())
        return address_name, address_number

    @classmethod
    def produce_price(cls, prices:list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['грн', ' ']) for f in prices]

    @staticmethod
    def produce_dataframe_filtration(df:pd.DataFrame, price:int, rooms:list) -> pd.DataFrame:
        """
        Static method which is dedicated to develop filtration of the dataframe
        Input:  df = dataframe of selected dataframe
        Output: we developed the dataframe to filtrate to values
        """
        df = df.loc[
            (df[Columns.column_price] <= price) & 
            (df[Columns.column_rooms].isin([int(f) for f in rooms]))        
        ]
        rooms_new = ', '.join(rooms)
        df[Columns.column_rooms] = rooms_new
        return df

    def produce_transform_dataframe(self, used_unique:set) -> pd.DataFrame:
        """
        Method which is dedicated to transform for the dataframe
        Input:  used_unique = unique value for the developed value
        Output: we created dataframe after parsing
        """
        self.folder_results = os.path.join(self.folder_storage, self.name)
        self.check_values_presence_folder()
        
        value_df = pd.DataFrame(
            {
                Columns.column_link: self.links,
                Columns.column_address: self.addresses,
                Columns.column_address_name: self.addresses_name,
                Columns.column_address_number: self.addresses_number,
                Columns.column_date: self.dates,
                Columns.column_price: self.prices,
                Columns.column_rooms: self.rooms,
                Columns.column_floor: self.floors,
                Columns.column_square: self.squares,
                Columns.column_address_add: self.addresses_add,
                Columns.column_desc: self.descs,
            }
        )
        value_df = self.produce_dataframe_filtration(
            value_df, 
            self.check_price, 
            self.check_rooms
        )

        self.create_dataframe(
            value_df, 
            self.create_dataframe_name(
                self.folder_results, 
                self.name, 
                used_unique
            )
        )
        return value_df