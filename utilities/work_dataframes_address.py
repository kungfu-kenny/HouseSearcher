import os
import pandas as pd
from datetime import datetime, timedelta
from utilities.work_dataframes import DevelopResults
from config import Columns


class DevelopAddress(DevelopResults):
    """
    class which is dedicated to develop selected dataframes 
    from the Address calculation
    """
    def __init__(
        self, name, addresses, links, dates, prices, descs, rooms, squares, floors, prices_square
    ) -> None:
        super(DevelopAddress, self).__init__()
        self.name = name
        self.links = links
        self.descs = descs
        self.addresses_full = addresses
        self.dates = self.produce_date(dates)
        self.prices = self.produce_price(prices)
        self.rooms = self.produce_room(rooms)
        self.squares = self.produce_square(squares)
        self.floors = self.produce_floor(floors)
        self.prices_sqr = self.produce_price_square(prices_square)
        self.addresses_name, self.addresses_number = self.produce_address_parse(addresses)

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
    def produce_date(cls, dates:list) -> list:
        """
        Class method which is dedicated to develop datetimes
        Input:  dates = list of dates
        Output: we developed list of the datetimes list
        """
        value_return = []
        for date in dates:
            date = date.replace('Обновлено', '').strip()
            date = date.replace('Сегодня', datetime.now().strftime('%Y-%m-%d'))
            date = date.replace('Вчера', (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'))
            value_return.append(date.strip())
        return value_return

    @classmethod
    def produce_room(cls, rooms:list) -> list:
        """
        Class method which is dedicated to develop room answer
        Input:  rooms = list of the parsed rooms
        Output: list of the selected values
        """
        return [', '.join(sorted(list(set(rooms)))) for _ in rooms]

    @classmethod
    def produce_square(cls, squares:list) -> list:
        """
        Class method which is dedicated to develop squares
        Input:  squares = list of squares
        Output: list of new squares
        """
        return [cls.produce_number(f, ['м2', ' ']) for f in squares] 

    @classmethod
    def produce_price(cls, prices:list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['₴', ' ']) for f in prices]

    @classmethod
    def produce_price_square(cls, prices_sqr:list) -> list:
        """
        Class method which is dedicated to develop prices of the square
        Input:  prices_sqr = list of square prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['₴ за кв. м.', ' ']) for f in prices_sqr]

    @classmethod
    def produce_floor(cls, floors: list) -> list:
        """
        Class method which is dedicated to develop floors
        Input:  floors = list of the floors
        Ouptut: list of the new floor
        """
        return [cls.produce_number(f.split('/')[0], ['/', ' ']) for f in floors]

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
                Columns.column_address: self.addresses_full,
                Columns.column_address_name: self.addresses_name,
                Columns.column_address_number: self.addresses_number,
                Columns.column_date: self.dates,
                Columns.column_price: self.prices,
                Columns.column_rooms: self.rooms,
                Columns.column_floor: self.floors,
                Columns.column_square: self.squares,
                Columns.column_square_price: self.prices_sqr,
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