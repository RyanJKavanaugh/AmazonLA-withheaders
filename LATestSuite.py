import unittest
# import HTMLTestRunner
import os
from LAVerifyMenuOptions import Verify_LA_Menu_Options
from LAVerifyHeaderLinks import Verify_Links
from LAVerifyCreateAndDeleteRoute import Verify_Login_And_Saving_Routes
from LAVerifyFDandTextSizes import Verify_Future_Dates_And_Text_Sizes
from LAVerifyUserLogin import Verify_Login
from LAVerifyMapLayers import Verify_Map_Layers
from LAVerifyLegend  import Verify_Legend_Data
from  LAVerifyPlace import Verify_Save_Place
import xlrd
import sys
from LaVariables import workbookNameData

workbook = xlrd.open_workbook(workbookNameData)
worksheet = workbook.sheet_by_index(0)
Jenkins = worksheet.cell(1, 4).value

# get the directory path to output report file
dir = os.getcwd()

# get all tests from SearchText and HomePageTest class
#   1
left_hand_menu = unittest.TestLoader().loadTestsFromTestCase(Verify_LA_Menu_Options)
#   2
header_links = unittest.TestLoader().loadTestsFromTestCase(Verify_Links)
#   3
future_dates_and_text_sizes = unittest.TestLoader().loadTestsFromTestCase(Verify_Future_Dates_And_Text_Sizes)
#   4
user_login = unittest.TestLoader().loadTestsFromTestCase(Verify_Login)
#   5
map_layers = unittest.TestLoader().loadTestsFromTestCase(Verify_Map_Layers)
#   6
create_and_delete_route = unittest.TestLoader().loadTestsFromTestCase(Verify_Login_And_Saving_Routes)
#   7
legend_data = unittest.TestLoader().loadTestsFromTestCase(Verify_Legend_Data)

# 8
create_route_API_check = unittest.TestLoader().loadTestsFromTestCase(Verify_Save_Place)

# create a test suite combining search_text and home_page_test
test_suite = unittest.TestSuite([create_route_API_check, left_hand_menu, header_links, future_dates_and_text_sizes, user_login, map_layers, create_and_delete_route, legend_data])

if Jenkins == True:
    # run the suite
    # unittest.TextTestRunner(verbosity=2).run(test_suite)
    #unittest.TextTestRunner(verbosity=2).run(test_suite)
    test_runner = unittest.TextTestRunner(resultclass=unittest.TextTestResult)
    result = test_runner.run(test_suite)
    sys.exit(not result.wasSuccessful())
else:
    # open the report file
    outfile = open(dir + "\SeleniumPythonTestSummary.html", "w")


    # configure HTMLTestRunner options
    runner = HTMLTestRunner.HTMLTestRunner(stream=outfile,title='Test Report', description='Acceptance Tests')

    # run the suite using HTMLTestRunner
    runner.run(test_suite)