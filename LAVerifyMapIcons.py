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
from pprint import pprint
from bs4 import  BeautifulSoup
import json
import jsonpickle
import xlrd
from pyvirtualdisplay import Display


def AdjustResolution():
    display = Display(visible=0, size=(800, 800))
    display.start()


workbook = xlrd.open_workbook('DataLA.xlsx')
worksheet = workbook.sheet_by_index(0)
url = worksheet.cell(1, 0).value
username = worksheet.cell(1, 1).value
password = worksheet.cell(1, 2).value
adjustResolution = worksheet.cell(1, 3).value

if adjustResolution == 1:
    AdjustResolution()


class Verify_Idaho_Map_Icons(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()

    def test_road_reports(self):
        print '\n' + "Verifying: Map Icons -> Road Reports"
        driver = self.driver
        driver.get('http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com//events_v1/api/eventMapFeatures?eventClassifications=roadReports')
        tgWebDict = {}

        data = driver.find_element_by_tag_name('body').text
        jsonData = json.loads(data)

        for item in jsonData:
            IDNum = item.get('id')
            imageName = item.get('representation').get('iconProperties').get('image')
            tgWebDict[IDNum] = imageName

        for roadReportsNum in tgWebDict:
            testURL = 'http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com//#roadReports/eventAlbum/' + str(roadReportsNum) + '?timeFrame=TODAY&layers=roadReports%2CwinterDriving%2CweatherWarnings%2CotherStates'
            driver.get(testURL)

            try:
                 mainImageWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'galleryPopup')))
                 assert driver.find_element_by_id('galleryPopup') #.is_displayed()
            except:
                print roadReportsNum
                assert False


    def test_cameras(self):
        print '\n' + "Verifying: MN Map Icons -> Cameras"
        driver = self.driver
        driver.get('http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com//cameras_v1/api/cameras?publicOnly=true')
        tgWebList = {}
        # 1. Grab all of the JSON from the API
        data = driver.find_element_by_tag_name('body').text
        jsonData = json.loads(data)
        # 2. Parse the Json into the dictionary
        for item in jsonData:
            IDNum = item.get('id')
            cameraName = item.get('name')
            tgWebList[IDNum] = cameraName
        # 3. Run through the dictionary to populate the web browser
        for cameraNum in tgWebList:
            testURL = 'http://crc-prod-id-wf-elb-382957924.us-west-2.elb.amazonaws.com/#cameras/albumView/' + str(cameraNum) + '?timeFrame=TODAY&layers=cameras'
            driver.get(testURL)
        # 4. Assert the web browser is correct by verifying the ablum view
            try:
                albumViewWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'galleryPopup')))
                assert driver.find_element_by_id('galleryPopup')  # .is_displayed()
            except:
                print cameraNum
                assert False

    def test_signs(self):
        print '\n' + "Verifying: MN Map Icons -> Signs"
        driver = self.driver
        driver.get('http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com/signs_v1/api/signs')
        tgWebList = {}

        data = driver.find_element_by_tag_name('body').text
        jsonData = json.loads(data)

        for item in jsonData:
            IDNum = item.get('idForDisplay')
            locationName = item.get('name')
            tgWebList[IDNum] = locationName

        for signNum in tgWebList:
            testURL = 'http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com/#signs/albumView/idahosigns*' + str(signNum) + '?timeFrame=TODAY&layers=signs'
            driver.get(testURL)
            try:
                albumViewWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'galleryPopup')))
                assert driver.find_element_by_id('galleryPopup')  # .is_displayed()
            except:
                print signNum
                assert False


    # def test_a_mountain_passes(self): ?????
    #     print '\n' + "Verifying: Idaho Map Icons -> Mountain Passes"
    #     driver = self.driver
    #     driver.get('http://idtg.carsprogram.org:80/mountainpasses_v1/api/passes')
    #     tgWebList = {}
    #
    #     data = driver.find_element_by_tag_name('body').text
    #     jsonData = json.loads(data)
    #
    #
    #     for item in jsonData:
    #         IDNum = item.get('id')
    #         locationName = item.get('name')
    #         tgWebList[IDNum] = locationName
    #
    #     for passesNum in tgWebList:
    #         if passesNum != 1:
    #             testURL = 'http://hb.511.idaho.gov/#mountainPasses/albumView/' + str(passesNum) + '?timeFrame=TODAY&layers=mountainPasses'
    #             driver.get(testURL)
    #             print testURL
    #             try:
    #                 albumViewWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'galleryPopup')))
    #                 assert driver.find_element_by_id('galleryPopup')  # .is_displayed()
    #             except:
    #                 driver.save_screenshot('testing123.png')
    #                 print passesNum
    #                 assert False
        # http://idtg.carsprogram.org/mountainpasses_v1/


    def test_weather_stations(self):
        print '\n' + "Verifying: MN Map Icons -> Weather Stations"
        driver = self.driver
        driver.get('http://idtg.carsprogram.org:80/rwis_v1/api/stations')
        tgWebList = {}

        data = driver.find_element_by_tag_name('body').text
        jsonData = json.loads(data)

        for item in jsonData:
            IDNum = item.get('id')
            locationName = item.get('name')
            tgWebList[IDNum] = locationName

        for stationsNum in tgWebList:
            testURL = 'http://crc-prod-mn-wf-elb-492694418.us-west-2.elb.amazonaws.com/#rwis/albumView/' + str(stationsNum) + '?timeFrame=TODAY&layers=rwis'
            driver.get(testURL)

            try:
                albumViewWait = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'galleryPopup')))
                assert driver.find_element_by_id('galleryPopup')  # .is_displayed()
            except:
                driver.save_screenshot('testing123.png')
                print passesNum
                assert False

    def tearDown(self):
         print "Test Completed"
         self.driver.quit()


if __name__ == '__main__':
    unittest.main()
