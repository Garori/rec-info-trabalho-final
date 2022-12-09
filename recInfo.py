import pandas as pd
from internetarchive import get_session
from internetarchive import download
import sys
sys.coinit_flags = 2  # COINIT_APARTMENTTHREADED
import shutil
from GUI import GUI
from pywinauto.application import Application
import psutil
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.edge.service import Service as EdgeService
import json
from openpyxl import load_workbook
import os
from urllib.request import urlopen as curl


class Crawler():
    def __init__(self):
        self.urls = ["barbie.com"]
        self.keywords = [""]
        self.startYear="2002"
        self.endYear = "2022"
        self.limitDomain = 100
        self.maxSize = (0,50)[type(0.1)==type(0.1)]
        self.downloadPath = r"C:\Users\Conde\Desktop\SWFS CRALERS\BARBIE JOAQUINA"
        self.numBaixadosDomain=0
        self.app = self.configurar_chrome()
        # self.app = self.configurar_edge()
        print(self.maxSize)


    def main(self):
        results = []
        for url in self.urls:
            if url[-1]!="/":
                url = url+"/"
            print(url)
            results.append(json.load(curl("http://web.archive.org/cdx/search/cdx?url="+url+"*&"+("","from="+self.startYear)[self.startYear.strip()!=""]+("","&to="+self.endYear)[self.endYear.strip()!=""]+"&output=json&limit=10000&filter=statuscode:200"+"&filter=mimetype:application/x-shockwave-flash"+"&showDupeCount=true&collapse=urlkey")))
        resultsArray=[]
        for num,domain in enumerate(results):
            resultsArray.append([])
            for index,line in enumerate(domain[1:]):
                _={}
                print("baixados "+str(self.numBaixadosDomain)+"/"+str(self.limitDomain)+" do domínio: "+self.urls[num])
                if self.numBaixadosDomain==self.limitDomain:
                    break
                elif self.searchKeyword(line):
                    for index2,i in enumerate(line):
                        if index2 != 2:
                            _.update({domain[0][index2] : i})
                        else:
                            _.update({domain[0][index2]: "https://web.archive.org/web/"+_["timestamp"]+"/"+i})
                    resultsArray[num].append(_)
        # resultsArray = sorted(resultsArray, key=lambda i: i['timestamp'], reverse=True)
        # print(resultsArray)
        # print(resultsArray[0][3]["original"])
        for domain in resultsArray:
            for site in domain:
                self.app.get(site["original"])
                sleep(5)
        sleep(1000)
        # print(domain[0])
        # curl(resultsArray[3]["original"])
        # s = get_session(config_file='./ia.ini')
        # s.mount_http_adapter()
        # search_results = s.search_items('levelupgames demo')
        # print(search_results)
        # for num, result in enumerate(search_results.iter_as_items()):
        #     print(result)
        # pass

        pass

    def searchKeyword(self, line):
        for keyword in self.keywords:
            if (line[2].lower().find(keyword.lower()) != -1) and float(line[-2])<(self.maxSize*(10**6)):
                self.numBaixadosDomain += 1
                print(line)
                return True
        return False

    def configurar_edge(self):
        # DEFINE AS OPCOES
        edge_options = webdriver.EdgeOptions()
        edge_options.add_argument("start-maximized")
        edge_options.add_argument("disable-infobars")
        app_state = {"recentDestinations": [{"id": "Save as PDF", "origin": "local",
                                             "account": ""}], "selectedDestinationId": "Save as PDF", "version": 2}
        profile = {"download.default_directory": self.downloadPath,
                   "savefile.default_directory": self.downloadPath,
                   "prompt_for_download": False,
                   'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
                   'download_restrictions': 0}
        # edge_options.add_argument("headless")
        # edge_options.add_argument("disable-gpu")
        edge_options.UseChromium = True
        # edge_options.add_argument("window-size=1920,1080")
        edge_options.add_experimental_option("useAutomationExtension", False)
        # edge_options.add_experimental_option("excludeSwitches")
        edge_options.add_experimental_option('prefs', profile)
        # driver = webdriver.Edge(service=EdgeService(
        #     "C:\edgedriver_win64\msedgedriver.exe"), options=edge_options)
        driver = webdriver.Edge(EdgeChromiumDriverManager().install(), options=edge_options)
        # "C:\edgedriver_win64\msedgedriver.exe", options=edge_options

        return driver

    def configurar_chrome(self):
        # DEFINE AS OPCOES
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-infobars")
        app_state = {"recentDestinations": [{"id": "Save as PDF", "origin": "local",
                                             "account": ""}], "selectedDestinationId": "Save as PDF", "version": 2}
        profile = {"download.default_directory": self.downloadPath,
                   "savefile.default_directory": self.downloadPath,
                   "prompt_for_download": False,
                   'printing.print_preview_sticky_settings.appState': json.dumps(app_state),
                   'download_restrictions': 0,
                   "safebrowsing.enabled": False}
        # chrome_options.add_argument("--kiosk-printing")
        chrome_options.add_experimental_option('prefs', profile)
        # self.driver = webdriver.Chrome(f'C:\\Users\\{getuser()}\\Selenium Webdriver\\chromedriver.exe', chrome_options=chrome_options)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=chrome_options)

        return driver



if __name__ == '__main__':
    programa = Crawler()
    programa.main()
