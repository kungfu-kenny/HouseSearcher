import sys, os
from parsing.parse_webdriver import ParseWebDriver
from parsing.parse_olx import ParseOlx
from parsing.parse_flatfy import ParseFlatfly


try:
    parse_web = ParseWebDriver()
    path_webdriver = parse_web.check_webdriver_main()
    #TODO add here values of the list of the districts
    # parse_olx = ParseOlx(path_webdriver, 'минская', 'Оболонский', [2, 3]).produce_search_results()
    parse_flatfy = ParseFlatfly(path_webdriver, [2, 3], 20000, 'мінська').produce_search_results()
except Exception as e:
    print(e)
    print('####################################################')
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)