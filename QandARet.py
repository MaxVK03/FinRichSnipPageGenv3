import time
import numpy as np
from serpapi import GoogleSearch
import pandas as pd
import openpyxl
from collections import defaultdict


class getQandA:
    # reading in the text from the Excel document
    DataIN = pd.read_excel(r'C:\\Users\Max von Klemperer\Desktop\PythExcels.xlsx')
    # print(DataIN)

    # Converts the Excel Columns into lists
    Mods = list(DataIN["Modifier"].values)
    Quests = list(DataIN["Question"].values)

    asdof = 1
    '''
    for i in Mods:
        if asdof % 3 > 0:
            Mods.remove(i)
        asdof += 1
    asdofs = 1
    for i in Quests:
        if asdofs % 3 > 0:
            Quests.remove(i)
        asdofs += 1
    '''
    QuestGroups = []
    Modifs = []
    Questsset = []
    numItems = []

    # All code below here is processing
    # Converting to a dictionary and then back to a list to get rid of duplicates

    Modifs = list(dict.fromkeys(Mods))
    CountI = 1
    # used this libray to allow dictionary's to accept arrays as items.
    # Used this method as it allows there to be a relationship between Questions and their modifiers
    # Bit of a mission at start but long term its the right way to go
    SortedDict = defaultdict(list)

    for i in range(0, len(Modifs) - 1):
        Its = []
        while Modifs[i] == Mods[CountI]:
            Its.append(Quests[CountI])
            CountI = CountI + 1
            # print(Quests[CountI])

        SortedDict[Modifs[i]].append(Its)

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

    Pos = 0
    for i in Modifs:
        SetOfQuest = str(SortedDict.get(i))
        SetOfQuest = SetOfQuest.replace("[", "")
        SetOfQuest = SetOfQuest.replace("]", "")
        SetOfQuest = SetOfQuest.replace('\'', "")
        ArSetOfQuest = SetOfQuest.split(", ")
        SubMod = i

        for z in ArSetOfQuest:
            if not ("None" in z):
                # print(i)
                quest = z
                print("Inp in google: " + quest)
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
                questions = []
                answers = []
                search = GoogleSearch(params)
                results = search.get_dict()

                for xq in results.get("organic_results")[0:8]:
                    if xq.get("link") not in Top4URL:
                        Top4URL.append(xq.get("link"))
                    # print("Here is a top 4 " + xq.get("link"))

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

                for z in range(0, len(answers)):
                    if not (str(answers[z]) == "None" or str(answers[z]) == "Cached"):
                        ConfirmedAns.append(answers[z].replace(";", ","))
                        ConfirmedQuest.append(questions[z].replace(";", ","))
                        ConfirmedOrig.append(quest)
                        SubMods.append(SubMod)
            Pos += 1