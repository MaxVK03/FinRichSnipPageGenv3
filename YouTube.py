import time
import numpy as np
from serpapi import GoogleSearch
import pandas as pd
import openpyxl
from collections import defaultdict


class getYout:
    # reading in the text from the the excel document
    # DataIN = pd.read_excel(r'C:\Users\Max von Klemperer\Desktop\PythExcels.xlsx')
    # print(DataIN)

    # Converts the Excel Columns into lists


    params = {
        "api_key": "6a9b9042c383a118a34f97cba712361dcc662b2a96fc5cd4def6e33cfe110641",
        "engine": "youtube",
        "search_query": "etoro safety information"
    }

    search = GoogleSearch(params)
    results = search.get_dict()
    vidRes = results.get("video_results")
    URLs = []
    for i in vidRes[0:4]:
        Lin = i.get("link")
        Lin = Lin.replace("watch?v=", "embed/")
        URLs.append(Lin)