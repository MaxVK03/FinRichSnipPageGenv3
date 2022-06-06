import time
import numpy as np
from serpapi import GoogleSearch
import pandas as pd
import openpyxl
from collections import defaultdict


class getGoogImage:
    # reading in the text from the the excel document
    # DataIN = pd.read_excel(r'C:\Users\Max von Klemperer\Desktop\PythExcels.xlsx')
    # print(DataIN)

    # Converts the Excel Columns into lists
    # cluster = list(DataIN["Cluster"].values)

    from serpapi import GoogleSearch

    params = {
        "api_key": "6a9b9042c383a118a34f97cba712361dcc662b2a96fc5cd4def6e33cfe110641",
        "engine": "google",
        "q": "etoro safety",
        "location": "Austin, Texas, United States",
        "google_domain": "google.com",
        "gl": "us",
        "hl": "en",
        "tbm": "isch"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    AllImg = results.get("images_results")
    FinImg = []

    for i in AllImg[0:4]:
        FinImg.append(i.get("original"))