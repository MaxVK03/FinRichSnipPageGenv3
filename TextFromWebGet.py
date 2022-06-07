from threading import Thread

from selenium.webdriver.chrome import webdriver
from selenium.webdriver.chrome.options import Options
from serpapi import GoogleSearch
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

import ClusterDet
import QandARet
import re
import requests
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class webCont:

    TextFromsites = ""
    params = {
        "engine": "google",
        "q": (ClusterDet.getClus.MainCluster + " information"),
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
    for i in TotURL[0:8]:
        print(i)
        options = Options()
        options.headless = True
        driver = webdriver.WebDriver(ChromeDriverManager().install(), options=options)
        driver.set_page_load_timeout(5)
        options = Options()
        options.headless = True
        if not ("jpost.com" in i or "wtkr" in i or "facebook" in i or "mensjournal" in i or "collinsdictionary" in i
                or "dictionary" in i):
            try:

                options = Options()
                options.headless = True
                driver.get(i)
                driver.set_page_load_timeout(5)
                # driver.manage().timeouts().pageLoadTimeout(15, TimeUnit.SECONDS)
                al = driver.find_elements_by_css_selector('p')
                for x in al[3:18]:
                    if len(x.text) > 50:
                        texttt = x.text
                        texttt = re.sub(r'\[.*?\]', '', texttt)
                        TextFromsites = TextFromsites + texttt
            except:
                xa += 1
                # driver.close()
        driver.close()

