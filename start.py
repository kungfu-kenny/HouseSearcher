from parsing.parse_webdriver import ParseWebDriver
from parsing.parse_olx import ParseOlx


try:
    parse_web = ParseWebDriver()
    path_webdriver = parse_web.check_webdriver_main()
    #TODO add here values of the list of the districts
    parse_olx = ParseOlx(path_webdriver, 'минская', 'Оболонский', [2, 3]).produce_search_results()
except Exception as e:
    print(e)
    print('####################################################')