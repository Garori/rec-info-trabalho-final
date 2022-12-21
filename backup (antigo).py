from urllib.parse import quote
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
from selenium.webdriver.chrome.service import Service as ChromeService
import json
from openpyxl import load_workbook
import os
from urllib.request import urlopen as curl


class Crawler():
    def __init__(self):
        #ENTRADAS
        self.keywordExclusive = 0                                                               # 1 para só pesquisar links com keywords qualquer outra coisa para pegar todos os links
        self.downloadPath = r"C:\Users\gabriel.c.fonseca\OneDrive - Accenture\Desktop\apagar"   # Caminho dos downloads
        self.query = "ragnarok online"                                                          # palavras a serem pesquisadas (deixar em branco com a DownloadAllFrom... ligada faz com que vc baie todos os swfs das urls adicionais)
        self.startYear="2004"                                                                   # ano de começo da pesquisa
        self.endYear = "2022"                                                                   # ano de fim da pesquisa
        self.limitDomain = 100                                                                  # Número máximo de downloads por domínio encontrado
        self.maxSize = 50                                                                       # tamanho máximo em MB  
        self.DownloadAllFromurlsImportantesAdicionais = 0                                       # (1 para ligar)ignora a pesquisa de urls na wikipedia e baixa tudo da lista de sites adicionais                                      
        self.urlsImportantesAdicionais = ["levelupgames.com.br"]                                # (OPCIONAL)
        #OUTRAS VARIÁVEIS
        self.numBaixadosDomain=0
        self.keywords = self.query.split(" ")
        self.numDownloads = len([1 for _ in os.scandir(self.downloadPath)])
        self.urls = [""]                    
        self.tries = 0                                                    
        self.app = self.configurar_chrome()
        # self.app = self.configurar_edge()
        # print(self.maxSize)


    def main(self):
        resultsArray = []
        results=[]
        if self.DownloadAllFromurlsImportantesAdicionais !=1:
            wikiSearchResults = json.load(curl("https://pt.wikipedia.org/w/api.php?action=query&list=search&srsearch="+quote(self.query)+"&format=json"))
            wikiPage = wikiSearchResults["query"]["search"][0]
            print(wikiPage)



            # print(wikiPageTitle)
            wikiRevisions = json.load(curl("https://pt.wikipedia.org/w/api.php?action=query&prop=revisions&titles="+quote(wikiPage["title"])+"&rvlimit=500&rvslots=main&rvprop=ids&rvstart="+self.startYear+"-12-31T00:00:00Z&rvend="+self.endYear+"-12-31T00:00:00Z&rvdir=newer&format=json"))
            wikiRevisions = wikiRevisions["query"]["pages"][str( wikiPage["pageid"])]["revisions"]
            print(len(wikiRevisions))
            extLinks=[]
            # revIds=""
            lastTemp=None
            for revisionIndex in range(0, len(wikiRevisions), 10):
                # print(str(wikiRevisions[revisionIndex]["revid"]))
                temp = json.load(curl("https://pt.wikipedia.org/w/api.php?action=parse&format=json&prop=externallinks&oldid="+str(wikiRevisions[revisionIndex]["revid"])+"&format=json"))
                # print(temp)
                if temp == lastTemp:
                    continue
                else:
                    for link in temp["parse"]["externallinks"]:
                        if link.find("https://web.archive.org/web/") != -1:
                            link = link.replace("https://web.archive.org/web/", "")
                            link = link[15:]
                            # print(link)
                        if link.find("http") != -1:
                            indexCorte = link.find("/", 8)
                            if indexCorte != -1:
                                link = link[:indexCorte]
                        else:
                            indexCorte = link.find("/")
                            if indexCorte != -1:
                                link = link[:indexCorte]
                        # print(link)
                        if link.find("google.com") == -1:
                            extLinks.append(link)
                    lastTemp=temp
                # print(extLinks)
                # revIds += str(wikiRevisions[revisionIndex]["revid"])+"|"

            if len(wikiRevisions)<500:
                temp = json.load(curl("https://pt.wikipedia.org/w/api.php?action=parse&format=json&prop=externallinks&oldid=" +str(wikiRevisions[-1]["revid"])+"&format=json"))
                if temp == lastTemp:
                    pass
                else:
                    for link in temp["parse"]["externallinks"]:
                        if link.find("https://web.archive.org/web/") != -1:
                            link = link.replace("https://web.archive.org/web/","")
                            link = link[15:]
                            # print(link)
                        if link.find("http")!=-1:
                            indexCorte = link.find("/",8)
                            if indexCorte !=-1:
                                link = link[:indexCorte]
                        else:
                            indexCorte = link.find("/")
                            if indexCorte !=-1:
                                link = link[:indexCorte]
                        if link.find("google.com")==-1:
                            extLinks.append(link)
            self.urls = list(set(extLinks))
            print("cabou")

            # sleep(1000)
            print(self.urls)
            for index,url in enumerate(self.urls):
                if url in self.urlsImportantesAdicionais:
                    self.urls.pop(index)

            # self.urls = sorted(self.urls, key=lambda i: (i.find(self.keywords[0]), 9999)[i.find(self.keywords[0])==-1])

            results = self.getWaybackURLS(self.urls)
        if len(self.urlsImportantesAdicionais)>0:
            adicionais = self.getWaybackURLS(self.urlsImportantesAdicionais)
            resultsArray.extend(adicionais)
        if len(results)>0:
            resultsArray.extend(results)

        print("----------------------------------------------------------------------------------------")
        print(resultsArray)

        for site in resultsArray:
            self.app.get(site)
            diretorio = os.scandir(self.downloadPath)
            # print(diretorio)
            numDownloadsLocal = 0
            for _ in diretorio:
                # print(_)
                numDownloadsLocal += 1
            while self.numDownloads != numDownloadsLocal-1 and self.tries <20:
                print("ainda não baixei o arquivo")
                print((self.numDownloads,numDownloadsLocal))
                diretorio = os.scandir(self.downloadPath)
                numDownloadsLocal = 0
                for _ in diretorio:
                    numDownloadsLocal += 1
                sleep(1)
                self.tries+=1
            self.numDownloads = numDownloadsLocal
            self.tries=0
        sleep(20)
        # print(domain[0])
        # curl(resultsArray[3]["original"])
        # s = get_session(config_file='./ia.ini')
        # s.mount_http_adapter()
        # search_results = s.search_items('levelupgames demo')
        # print(search_results)
        # for num, result in enumerate(search_results.iter_as_items()):
        #     print(result)
        # pass

    def getWaybackURLS(self,urls):
        results = []
        for url in urls:
            if url[-1] != "/":
                url = url+"/"
            print(url)
            results.append(json.load(curl("http://web.archive.org/cdx/search/cdx?url="+quote(url)+"*&"+("", "from="+self.startYear)[self.startYear.strip() != ""]+("", "&to="+self.endYear)[
                           self.endYear.strip() != ""]+"&output=json&limit=10000&filter=statuscode:200"+"&filter=mimetype:application/x-shockwave-flash"+"&showDupeCount=true&collapse=urlkey")))
        resultsArray = []
        print(results)
        for num, domain in enumerate(results):
            # resultsArray.append([])
            for index, line in enumerate(domain[1:]):
                link = {}
                # print("baixados "+str(self.numBaixadosDomain)+"/"+str(self.limitDomain)+" do domínio: "+self.urls[num])
                if self.numBaixadosDomain == self.limitDomain:
                    break
                elif self.searchKeyword(line):
                    resultsArray.append(
                        "https://web.archive.org/web/"+line[1]+"/"+line[2])

        resultsArray = sorted(resultsArray, key=lambda i: (i.find(self.keywords[0]), 9999)[i.find(self.keywords[0]) == -1])
        return resultsArray

    def searchKeyword(self, line):
        for keyword in self.keywords:
            if self.keywordExclusive == 1 and (line[2].lower().find(keyword.lower()) != -1) and float(line[-2]) < (self.maxSize*(10**6)):
                self.numBaixadosDomain += 1
                print(line)
                return True
            elif self.keywordExclusive != 1 and float(line[-2]) < (self.maxSize*(10**6)):
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
        driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=edge_options)
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
                   "safebrowsing.enabled": False,
                   "safebrowsing.disable_download_protection":True,
                   "profile.default_content_settings.popups":0
                   }
        chrome_options.add_argument("--safebrowsing-disable-download-protection")
        chrome_options.add_experimental_option('prefs', profile)
        # self.driver = webdriver.Chrome(f'C:\\Users\\{getuser()}\\Selenium Webdriver\\chromedriver.exe', chrome_options=chrome_options)
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_options)

        return driver



if __name__ == '__main__':
    programa = Crawler()
    programa.main()
