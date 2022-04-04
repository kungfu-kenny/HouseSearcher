import os
from pprint import pprint
import pandas as pd
from datetime import datetime, timedelta
from utilities.work_dataframes import DevelopResults
from config import Columns


class DevelopOlx(DevelopResults):
    """
    class which is dedicated to develop selected dataframes 
    from the Olx calculation
    """
    def __init__(self, name, addresses, links, dates, prices, addresses_add) -> None:
        super(DevelopOlx, self).__init__()
        self.name = name
        self.links = links
        self.addresses = addresses
        self.addresses_add = addresses_add
        self.dates = self.produce_date(dates)
        self.prices = self.produce_price(prices)

    @classmethod
    def produce_price(cls, prices:list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        return [
            cls.produce_number(f, ['грн.', '\nДоговорная', '$', ' ']) 
            for f in [f if f else '-1' for f in prices]
        ]

    @classmethod
    def produce_date(cls, dates: list) -> list:
        return_dates = []
        for date in dates:
            date = date.replace(
                'Сегодня', 
                datetime.now().strftime('%d %B')
            )
            date = date.replace(
                'Вчера', 
                (datetime.now() - timedelta(days=1)).strftime('%d %B')
            )
            return_dates.append(date)
        return return_dates

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
                Columns.column_name: self.addresses,
                Columns.column_address_add: self.addresses_add,
                Columns.column_date_created: self.dates,
                Columns.column_price: self.prices,
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