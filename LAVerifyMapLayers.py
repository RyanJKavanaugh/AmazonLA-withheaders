# coding=utf-8
from selenium import webdriver
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import unittest
import xlrd
from pprint import pprint
from LaVariables import workbookNameData
from pyvirtualdisplay import Display
# -*- coding: utf-8 -*-

# Required function for making test work in Jenkins
def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


workbook = xlrd.open_workbook(workbookNameData)
worksheet = workbook.sheet_by_index(0)
url = worksheet.cell(1, 0).value
adjustResolution = worksheet.cell(1, 3).value

if adjustResolution == 1:
    AdjustResolution()

verifyMapLayersWorksheet = workbook.sheet_by_index(1)

# Lists for holding Map Layer Data from Spreadsheet
itemText = []
itemLink = []
itemXpath = []

# Loop to gather all relevant info for drop down layers
for x in range (0, 9):
    itemText.append(verifyMapLayersWorksheet.cell(x + 1, 1).value)
    itemLink.append(verifyMapLayersWorksheet.cell(x + 1, 2).value)
    itemXpath.append(verifyMapLayersWorksheet.cell(x + 1, 3).value)

# Function to verify drop down layers
def Verify_Layer_Drop_Down_Item(driver, xPath, itemText, itemLink):
    item = driver.find_element_by_xpath(xPath)
    itemHTML = item.get_attribute('innerHTML')
    if (itemText in itemHTML) and (itemLink in itemHTML):
        return True
    else:
        return False

# Unit test for reporting status of test back to team
class Verify_Map_Layers(unittest.TestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_extension('ModHeader_v2.1.2.crx')
        self.driver = webdriver.Chrome(chrome_options=options)


    def test_presence_of_correct_layers(self):
        driver = self.driver
        driver.get("chrome-extension://idgpnmonknjnojddfkpgkljpfnnfcklj/icon.png")
        driver.execute_script(
            "localStorage.setItem('profiles', JSON.stringify([{                " +
            "  title: 'Selenium', hideComment: true, appendMode: '',           " +
            "  headers: [                                                      " +
            "    {enabled: true, name: 'Host', value: 'hb.511la.org', comment: ''}, " +
            "  ],                                                              " +
            "  respHeaders: [],                                                " +
            "  filters: [{enabled: true, type: 'urls', urlPattern : '*//*crc-prod-la-tg-elb-502362459.us-west-2.elb.amazonaws.com/*' , comment: ''},]                                                     " +
            "}]));                                                             ")
        driver.get(url)


        dropDownMenuWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'layers-menu-dropdown-button')))
        driver.find_element_by_id('layers-menu-dropdown-button').click()

        itemWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="layerSelector"]/ul/li[1]/a/span/img[1]')))
        # 1. First Item Verification: LA Road Reports
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[0], itemText[0], itemLink[0]), "LA Road Reports Is Faulty"
        # 2. Second Item Verification: LA Construction
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[1], itemText[1], itemLink[1]), "LA Construction Is Faulty"
        # 3. Third Item Verification: LA Waze Reports
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[2], itemText[2], itemLink[2]), "LA Waze Reports Is Faulty"
        # 4. Fourth Item Verification: Weather Warnings
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[3], itemText[3], itemLink[3]), "LA Weather Warnings Is Faulty"
        # 5. Fifth Item Verification: Ferry Status
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[4], itemText[4], itemLink[4]), "LA Ferry Status Is Faulty"
        # 6. Sixth Item Verification: Flooding/Ice
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[5], itemText[5], itemLink[5]), "LA Flooding/Ice Is Faulty"
        # 7. Seventh Item Verification: Cameras
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[6], itemText[6], itemLink[6]), "LA Cameras Are Faulty"
        # 8. Eighth Item Verification: Google Speeds and Incidents
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[7], itemText[7], itemLink[7]), "Google Speeds and Incidents Are Faulty"
        # 9. Ninth Item Verification: Other States' Info
        assert Verify_Layer_Drop_Down_Item(driver, itemXpath[8], itemText[8], itemLink[8]), "Other States' Info Are Faulty"


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    print ('\n') + "Verifying TG Web Map Layers" + '\n'
    unittest.main()