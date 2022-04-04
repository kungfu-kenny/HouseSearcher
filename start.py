import sys, os
from parsing.parse_webdriver import ParseWebDriver
from parsing.parse_olx import ParseOlx
from parsing.parse_domria import ParseDomria
from parsing.parse_flatfy import ParseFlatfly
from parsing.parse_rieltor import ParseRieltor
from parsing.parse_address import ParseAddress
from utilities.work_values_input import StringBasicTransform
from utilities.work_directories import develop_name_additional
from utilities.work_dataframes import DevelopResults


#TODO add here the parallelization to the end
try:
    parse_web = ParseWebDriver()
    path_webdriver = parse_web.check_webdriver_main()

    data_ukr = StringBasicTransform().get_default_data()
    data_rus = StringBasicTransform().get_default_data('rus')
    city_ukr, insert, district_ukr, rooms, price = StringBasicTransform(
        'ukr', 
        data_ukr.get('city'), 
        data_ukr.get('insert'), 
        data_ukr.get('district'), 
        data_ukr.get('rooms'), 
        data_ukr.get('price')
    ).main()
    city_rus, insert_rus, district_rus, *_ = StringBasicTransform(
        'rus', 
        data_rus.get('city'), 
        data_rus.get('insert'), 
        data_rus.get('district'), 
        data_rus.get('rooms'), 
        data_rus.get('price')
    ).main()
    used_results = develop_name_additional()
    
    parse_olx = ParseOlx(path_webdriver, city_ukr, insert, district_rus, rooms, price).produce_search_results(used_results)
    parse_domria = ParseDomria(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results(used_results)
    parse_rieltor = ParseRieltor(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results(used_results)
    parse_flatfy = ParseFlatfly(path_webdriver, city_ukr, insert, district_ukr, rooms, price).produce_search_results(used_results)
    parse_address = ParseAddress(path_webdriver, city_rus, '', district_rus, rooms, price).produce_search_results(used_results)
    
    DevelopResults().produce_result(
        [
            parse_olx, 
            parse_rieltor, 
            parse_flatfy, 
            parse_address,
            parse_domria
        ], 
        used_results
    )

except Exception as e:
    print(e)
    print('####################################################')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
