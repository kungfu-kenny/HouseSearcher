import os
import pandas as pd
from datetime import datetime, timedelta
from utilities.work_dataframes import DevelopResults
from config import Columns


class DevelopFlatfy(DevelopResults):
    """
    class which is dedicated to develop selected dataframes 
    from the Flatfy calculation
    """

    def __init__(
        self, name, addresses, links, dates, prices, descs, rooms, squares, floors, addresses_ful, price_sqr, subdists, years, types, repairs
    ) -> None:
        super(DevelopFlatfy, self).__init__()
        self.name = name
        self.links = links
        self.descs = descs
        self.types = types
        self.repairs = repairs
        self.addresses = [self.produce_address_removal(f) for f in addresses]
        self.subdists = subdists
        self.addresses_add = addresses_ful
        self.dates, self.dates_created = self.produce_date(dates, years)
        self.prices = self.produce_price(prices)
        self.rooms = self.produce_room(rooms)
        self.squares, self.squares_split = self.produce_square(squares)
        self.floors = self.produce_floor(floors)
        self.prices_sqr = self.produce_price_square(price_sqr)
        self.addresses_name, self.addresses_number = self.produce_adress_parse(self.addresses)

    @staticmethod
    def produce_address_removal(value_name:str) -> str:
        """
        Static method which is dedicated to removal address types
        Input:  value_name = name where to remove
        Output: 
        """
        for f in ['ул.', 'просп.', 'пер.']:
            value_name = value_name.replace(f, '')
        return value_name.strip()

    @classmethod
    def produce_adress_parse(cls, addresses:list) -> set:
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
            # address_str = cls.produce_adress_removal(address_str)
            address_name.append(address_str.strip())
            address_number.append(address_int.strip())
        return address_name, address_number

    @classmethod
    def produce_square(cls, squares:list) -> set:
        """
        Static method which is dedicated to develop squares
        Input:  squares = list of squares
        Output: list of new squares / list of summary squares
        """
        squares = [f.replace('м²','').strip() for f in squares]
        squares_sum = []
        for f in squares:
            squares_sum.append(
                sum(float(k.strip()) for k in f.split('/'))
            )
        return squares_sum, squares

    @classmethod
    def produce_date(cls, dates:list, years:list) -> list:
        """
        Class method which is dedicated to develop datetimes
        Input:  dates = list of dates
        Output: we developed list of the datetimes list
        """
        value_dates, value_dates_created = [], []
        for date, year in zip(dates, years):
            date_split = date.split('Создано')
            value_date, value_date_created = date_split
            value_date = value_date.replace(
                'сегодня в', 
                datetime.now().strftime('%Y-%m-%d')
            )
            value_date = value_date.replace(
                'вчера в', 
                (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            )
            value_date_created = value_date_created.replace(
                'сегодня в',
                datetime.now().strftime('%d %B')
            )
            value_date_created = value_date_created.replace(
                'вчера в',
                (datetime.now() - timedelta(days=1)).strftime('%d %B')
            )
            value_dates.append(value_date.strip())
            value_dates_created.append(f"{value_date_created.strip().title()} {year}")
        return value_dates, value_dates_created

    @classmethod
    def produce_price(cls, prices:list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['грн', ' ']) for f in prices]

    @classmethod
    def produce_price_square(cls, prices_sqr:list) -> list:
        """
        Class method which is dedicated to develop prices of the square
        Input:  prices_sqr = list of square prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['грн за м²', ' ']) for f in prices_sqr]
        
    @classmethod
    def produce_floor(cls, floors:list) -> list:
        """
        Class method which is dedicated to develop floors
        Input:  floors = list of the floors
        Ouptut: list of the new floor
        """
        return [int(f.strip().split(' ')[0]) for f in floors]

    @classmethod
    def produce_room(cls, rooms:list) -> list:
        """
        Class method which is dedicated to develop room answer
        Input:  rooms = list of the parsed rooms
        Output: list of the selected values
        """
        rooms = [f.strip().split(' ')[0] for f in rooms]
        rooms_all = ', '.join(sorted(list(set(rooms))))
        return [rooms_all for _ in rooms]

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
                Columns.column_square_price: self.prices_sqr,
                Columns.column_types: self.types,
                Columns.column_types_repair: self.repairs,
                Columns.column_subdists: self.subdists,
                Columns.column_address_add: self.addresses_add,
                Columns.column_date_created: self.dates_created,
                Columns.column_square_split: self.squares_split,
                Columns.column_desc: self.descs,
            }
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
