import sys, os
from parsing.parse_webdriver import ParseWebDriver
from parsing.parse_olx import ParseOlx
from parsing.parse_domria import ParseDomria
from parsing.parse_flatfy import ParseFlatfly
from parsing.parse_rieltor import ParseRieltor
from parsing.parse_address import ParseAddress
from utilities.work_values_input import StringBasicTransform


try:
    parse_web = ParseWebDriver()
    path_webdriver = parse_web.check_webdriver_main()

    #TODO add here values of the list of the districts
    city_ukr, insert, district_ukr, rooms, price = StringBasicTransform('ukr', 'київ', 'мінська', 'Оболонський', [2, 3], 23000).main()
    city_rus, insert_rus, district_rus, *_ = StringBasicTransform('rus', 'київ', 'минская', 'Оболонський', [2, 3], 23000).main()
    
    #TODO refactor all of these data parsers
    # parse_olx = ParseOlx(path_webdriver, city_ukr, insert, district_rus, rooms, price).produce_search_results()
    # parse_flatfy = ParseFlatfly(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results()
    # parse_rieltor = ParseRieltor(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results()
    # parse_domria = ParseDomria(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results()
    parse_adress = ParseAddress(path_webdriver, city_rus, '', district_rus, rooms, price).produce_search_results()

except Exception as e:
    print(e)
    print('####################################################')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)