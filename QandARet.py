import time
import numpy as np
import requests
from serpapi import GoogleSearch
import pandas as pd
import openpyxl
from collections import defaultdict
import ClusterDet
class getQandA:
    global answers
    url = "https://ask-your-question.p.rapidapi.com/question"
    querystring = {"query": ClusterDet.getClus.MainCluster}
    headers = {
        "X-RapidAPI-Host": "ask-your-question.p.rapidapi.com",
        "X-RapidAPI-Key": "a427bdc201msh61ea63ec5feeebcp1f72b0jsn0e7c21fe23cc"
    }
    DictQ = {}
    response = requests.request("GET", url, headers=headers, params=querystring)

    # print(response.text)
    respArr = response.text.split("\"type\"")
    ansArr = []
    for i in respArr[0:3]:
        currArr = []
        # print(i)
        quest = ""
        if i.find("answer") > -1:
            quest = i[:i.find("answers")].replace(":", "").replace("\"", "").replace(",", "")
            sansArr = i[i.find("answer"):]
            ansArr = sansArr.split(",")
        for z in ansArr:
            currArr.append(z.replace("answers\":[", "").replace("\"", "").replace("]}", "").replace("{", ""))

        DictQ[quest] = currArr
    QID = 0
    Anss = []
    ConfirmedAns = []
    ConfirmedQuest = []
    ConfirmedOrig = []
    SubMods = []
    ArSetOfQuest = []
    Top4URL = []
    # All Processing is done above here
    # All Q and A code is below here
    questions = []
    answers = []
    questions = []
    answers = []
    for i in DictQ.keys():
        for x in DictQ.get(i)[0:1]:
            quest = x
            print("Inp in google : " + quest)
            time.sleep(5)
            params = {
                "engine": "google",
                "q": quest,
                "location": "Austin, Texas, United States",
                "google_domain": "google.com",
                "gl": "us",
                "hl": "en",
                "no_cache": "True",
                "api_key": "6a9b9042c383a118a34f97cba712361dcc662b2a96fc5cd4def6e33cfe110641",
            }

            ansCount = 0
            questCount = 0

            search = GoogleSearch(params)
            results = search.get_dict()
            try:
                for xq in results.get("organic_results")[0:8]:
                    if xq.get("link") not in Top4URL:
                        Top4URL.append(xq.get("link"))
                    # print("Here is a top 4 " + xq.get("link"))
            except:
                print()
            try:
                for i in results.get("related_questions"):

                    try:
                        Liz = i.get("list")
                        tz3 = ""
                        for j in Liz:
                            if not ("cache" in j):
                                # print(j)
                                tz3 = tz3 + str(j)
                        answers.append(tz3)
                        questions.append(i.get("question"))
                    except:
                        answers.append(i.get("snippet"))
                        questions.append(i.get("question"))

            except:
                print("No results found inside of related question")

            try:
                ansBox = results.get("answer_box")
                # print(ansBox)
                # print(ansBox.get('result'))

                while True:
                    try:
                        # print(ansBox.get('result'))
                        ListAnsBox = []
                        AnsList = ansBox.get('list')
                        # print(AnsList)
                        tex2 = ""
                        for i in AnsList:
                            if not ("cache" in i):
                                tex2 = tex2 + i
                        answers.append(tex2)
                        questions.append(quest)
                        break
                    except:
                        pass
                    try:
                        answers.append(ansBox.get("snippet"))
                        questions.append(quest)

                        break
                    except:
                        pass
                    try:
                        # print(ansBox.get('result'))
                        answers.append(ansBox.get('result'))
                        questions.append(quest)

                        break
                    except:
                        pass
                    try:
                        # questions.append(quest)
                        # answers.append(ansBox.get("list"))

                        break
                    except:
                        pass

                    try:
                        # print(ansBox.get('title'))
                        questions.append(quest)
                        answers.append(ansBox.get('title'))

                        pass
                    except:
                        break
            except:
                print("No results found for answer box")

        # print(quest)
    finAns = answers
    finQuest = questions
