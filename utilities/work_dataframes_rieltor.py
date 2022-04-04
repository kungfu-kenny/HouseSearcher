import os
from pprint import pprint
import pandas as pd
from utilities.work_dataframes import DevelopResults
from config import Columns


class DevelopRieltor(DevelopResults):
    """
    class which is dedicated to develop dataframe 
    from the rieltor values
    """
    def __init__(
        self, name, addresses, links, prices, descs, rooms, further, subway, commission, types, district, check_price, check_district
    ) -> None:
        super(DevelopRieltor, self).__init__()
        replace_value = 'fgfijogdijgofrdtlcsuzfd;gijolsvkxbczfdsgial;okz'
        replace_list = ['кімнати,', 'кімната,', 'кімнат,', ' · ', 'поверх', 'м²', '.,']
        self.name = name
        self.links = links
        self.descs = descs
        self.subway = [f.replace('(M)', '').strip() for f in subway]
        self.check_price = check_price
        self.types_site = [f.capitalize() for f in types]
        self.commission = [f.capitalize() for f in commission]
        self.prices = self.produce_price(prices)
        self.districts = self.produce_district(district)
        self.check_district = check_district.capitalize().strip()
        self.rooms = [', '.join(sorted(rooms)) for _ in addresses]
        self.addresses = [self.produce_address_removal(f) for f in addresses]
        self.addresses_name, self.addresses_number = self.produce_address_parse(self.addresses)
        self.rooms, self.floors, self.types, self.square, self.square_split \
            = self.produce_further(further, replace_list, replace_value)
        
    @classmethod
    def produce_further(cls, further:list, replace_list:list, replace_value:list) -> list:
        """
        Static method which is dedicated to develop squares
        Input:  squares = list of squares
                replace_list = list which to replace
                replace_value = value to give on the change
        Output: list of new squares
        """
        rooms, floors, types, squares, squares_sqlit = [], [], [], [], []
        for furth in further:
            for rep in replace_list:
                furth = furth.replace(rep, replace_value)
            room, floor, _, typ, square_sp, *_ = furth.split(replace_value)
            types.append(typ.strip() if '/' not in typ else '')
            squares_sqlit.append(square_sp.strip())
            rooms.append(cls.produce_number(room, [' ']))
            floors.append(cls.produce_number(floor, [' ']))
            squares.append(sum(float(k.strip()) for k in square_sp.split('/') if k))
        return [', '.join(str(f) for f in list(set(rooms))) for _ in further], \
                floors, types, squares, squares_sqlit

    @staticmethod
    def produce_district(district:list) -> list:
        """
        Static method which is dedicated to develop selected district
        Input:  district = list of selected districts
        Output: list of parsed district values
        """
        return [f.replace('р-н', '').strip() for f in district]
    
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
    def produce_price(cls, prices: list) -> list:
        """
        Class method which is dedicated to develop prices
        Input:  prices = list of prices
        Output: list of new prices
        """
        return [cls.produce_number(f, ['грн/міс', '$/міс', ' ']) for f in prices]

    @staticmethod
    def produce_dataframe_filtration(df:pd.DataFrame, price:int, district:str) -> pd.DataFrame:
        """
        Static method which is dedicated to develop filtration of the dataframe
        Input:  df = dataframe of selected dataframe
                price = price which to check
                district = district value to use
        Output: we developed the dataframe to filtrate to values
        """
        district = district.capitalize()
        df = df.loc[
            (df[Columns.column_price] <= price) & 
            (df[Columns.column_subdists] == district)        
        ]
        #TODO think about it
        df.pop(Columns.column_subdists)
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
                Columns.column_price: self.prices,
                Columns.column_rooms: self.rooms,
                Columns.column_floor: self.floors,
                Columns.column_square: self.square,
                Columns.column_square_split: self.square_split,
                Columns.column_subway: self.subway,
                Columns.column_subdists: self.districts,
                Columns.column_types_repair: self.types,
                Columns.column_commission: self.commission,
                Columns.column_types_site: self.types_site,
                Columns.column_desc: self.descs,
            }
        )
        value_df = self.produce_dataframe_filtration(
            value_df, 
            self.check_price, 
            self.check_district
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