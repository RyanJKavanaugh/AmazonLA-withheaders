# coding=utf-8
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common import action_chains, keys
from selenium.webdriver.common.by import By
import time
import unittest
import xlrd
import requests
import json
from pyvirtualdisplay import Display
from LaVariables import workbookNameData
# -*- coding: utf-8 -*-

def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


workbook = xlrd.open_workbook(workbookNameData)
worksheet = workbook.sheet_by_index(0)
url = worksheet.cell(1, 0).value
username = worksheet.cell(1, 1).value
password = worksheet.cell(1, 2).value
adjustResolution = worksheet.cell(1, 3).value


if adjustResolution == 1:
    AdjustResolution()


class Verify_Save_Place(unittest.TestCase):


    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_extension('ModHeader_v2.1.2.crx')
        self.driver = webdriver.Chrome(chrome_options=options)
        self.driver.maximize_window()


    def test_login_route_creation_and_deletion(self):
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

        # HEAD TO THE SEARCH MENU AND SAVE A PLACE
        try:
            searchButonWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'searchBtn')))
        except:
            searchButonWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'searchBtn')))

        driver.find_element_by_id('searchBtn').click()

        placeNameTxtWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'placeNameTxt')))
        placeNameTxtElem = driver.find_element_by_id('placeNameTxt')
        placeNameTxtElem.send_keys('Alexandria, LA, United States')
        placeNameTxtElem.send_keys(Keys.RETURN)

        saveAreaLinkWait = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "saveAreaLink")))

        # 777 MAYBE TALK TO DEV ABOUT THIS ONE:
        driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click()

        # LOGIN FOR SAVING THE ROUTE
        pageLoadWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.ID, 'userAccountEmail')))
        driver.find_element_by_id('userAccountEmail').send_keys(username) # Login
        driver.find_element_by_id('userAccountPassword').send_keys(password)
        driver.find_element_by_id('userAccountPassword').submit()

        saveAreaLinkWait2 = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="leftPanelContent"]/div/div[3]/a')))
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="leftPanelContent"]/div/div[3]/a').click()

        saveAreaButtonWait = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="saveAreaForm"]/button')))
        driver.find_element_by_xpath('//*[@id="saveAreaForm"]/button').click()  # Clicking the submit button

        userInfo = {"userId":"ryan.kavanaugh@crc-corp.com","password":"test"}
        authTokenURL = 'http://latg.carsprogram.org:80/publicaccounts_v1/api/authTokens'

        myResponse = requests.post(authTokenURL, json=userInfo)
        jData = json.loads(myResponse.content)
        authToken = jData.get('id')
        accountID = jData.get('accountId')

        # This section gets the user's current saved places
        #       This allows us to create places and make sure they hit the api & that we can create stuff via the API
        #       and then check to see that the saved places showed up on the TG-Web site

        customAreasAPIUrl = 'http://latg.carsprogram.org:80/publicaccounts_v1/api/accounts/' + str(accountID) + '/customAreas?authTokenId=' + str(authToken)
        customAreaJson = requests.get(customAreasAPIUrl)

        data = customAreaJson.json()

        if len(data) > 0:
            #print data[0]
            placeName = data[0].get('name')
            placeID = data[0].get('id')
            print placeName

        assert placeName == 'Alexandria, LA, United States'

        # Wipe clean the event after we have asserted that it was created via the interface in the API
        deleteUrl = 'https://hb.511la.org/tgpublicaccounts/api/accounts/15466/customAreas/' + str(placeID) + '?authTokenId=' + str(authToken)
        deleteItem = requests.delete(deleteUrl)


    def tearDown(self):
        self.driver.quit()


if __name__ == '__main__':
    unittest.main()