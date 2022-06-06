from threading import Thread

from selenium.webdriver.chrome import webdriver
from serpapi import GoogleSearch
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import QandARet
import re
import requests
from webdriver_manager.chrome import ChromeDriverManager


class webCont:

    '''
    #URLToGet = QandARet.getQandA.Top4URL
    TextFromsites = ""
    #DataIN = pd.read_excel(r'C:\Users\Max von Klemperer\Desktop\PythExcels.xlsx')
    # print(DataIN)
    # Converts the Excel Columns into lists
    #cluster = list(DataIN["Cluster"].values)
    params = {
        "engine": "google",
        "q": ("eToro" + " safety information"),
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "no_cache": "True",
        "api_key": "6a9b9042c383a118a34f97cba712361dcc662b2a96fc5cd4def6e33cfe110641",
    }
    ansCount = 0
    questCount = 0
    questions = []
    answers = []
    search = GoogleSearch(params)
    results = search.get_dict()
    TotURL = []
    for qw in results.get("organic_results"):
        TotURL.append(qw.get("link"))
    xa = 8
    for i in TotURL[0:15]:
        driver = webdriver.WebDriver(ChromeDriverManager().install())
        if not ("jpost.com" in i or "wtkr" in i or "mensjournal" in i or "collinsdictionary" in i or "dictionary" in i):
            try:
                driver.get(i)
                driver.set_page_load_timeout(5)
                # driver.manage().timeouts().pageLoadTimeout(15, TimeUnit.SECONDS)
                al = driver.find_elements_by_css_selector('p')
                for x in al[1:7]:
                    if len(x.text) > 50:
                        texttt = x.text
                        texttt = re.sub(r'\[.*?\]', '', texttt)
                        TextFromsites = TextFromsites + texttt
            except:
                xa += 1
                # driver.close()
        driver.close()
        '''
