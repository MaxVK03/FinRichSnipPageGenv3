import re
import mysql.connector
from MySQLdb._exceptions import Error
import torch
from transformers import T5ForConditionalGeneration, T5Tokenizer
import os
import openai

openai.api_key = "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"

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = T5ForConditionalGeneration.from_pretrained("Michau/t5-base-en-generate-headline")
tokenizer = T5Tokenizer.from_pretrained("Michau/t5-base-en-generate-headline")
model = model.to(device)

ClusterData = []
ImageData = []
NewsData = []
pageData = []
QandAData = []
YouTubeData = []


class MakePage:
    try:
        connection = mysql.connector.connect(host='34.203.153.217',
                                             database='RichSnipPageGeneration',
                                             user='root',
                                             password='?w$D<U):;(f]3n3[')

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Connected to MySQL Server version ", db_Info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

            cursor.execute("SELECT * FROM clusters")
            ClusterData = cursor.fetchall()
            cursor.execute("SELECT * FROM images")
            ImageData = cursor.fetchall()
            cursor.execute("SELECT * FROM newstext")
            NewsData = cursor.fetchall()
            cursor.execute("SELECT * FROM pagetext")
            pageData = cursor.fetchall()
            cursor.execute("SELECT * FROM qandout")
            QandAData = cursor.fetchall()
            cursor.execute("SELECT * FROM youtubevids")
            YouTubeData = cursor.fetchall()

    except Error as e:
        print("Error while connecting to MySQL", e)

    ClusterID = 1
    ClusterName = ""

    for i in ClusterData:
        if int(i[0]) == ClusterID:
            # print(i[0])
            ClusterName = i[1]

    for i in range(1, 10):
        for i in ImageData:
            if not (int(i[0]) == ClusterID):
                ImageData.remove(i)

    for i in range(1, 10):
        for i in pageData:
            if not (int(i[0]) == ClusterID):
                pageData.remove(i)

    for i in QandAData:
        if not (int(i[0]) == ClusterID):
            # print(i[0])
            QandAData.remove(i)

    for i in QandAData:
        if not (int(i[0]) == ClusterID):
            QandAData.remove(i)

    for i in range(1, 100):
        for i in QandAData:
            if not (int(i[0]) == ClusterID):
                QandAData.remove(i)

    for i in QandAData:
        if not (int(i[0]) == ClusterID):
            QandAData.remove(i)

    for i in QandAData:
        if i[0] == 1:
            QandAData.remove(i)

    for i in QandAData:
        if i[1] == 1:
            QandAData.remove(i)

    for i in YouTubeData:
        if not (int(i[0]) == ClusterID):
            YouTubeData.remove(i)
    for i in range(1, 10):
        for i in YouTubeData:
            if not (int(i[0]) == ClusterID):
                YouTubeData.remove(i)

    with open(r"HeaderHTML") as f:
        contents = f.readlines()

    texxxxt = ""
    for i in contents:
        texxxxt = texxxxt + i

    texxxxt = texxxxt.replace("12354123123", ClusterName + " All you need to know")
    FinalHTML = ""
    FinalHTML = texxxxt + "\n\n"

    ClusterName = r"<h1>" + ClusterName + " - All you need to know" + r'</h1><br>' + '\n\n'
    FinalHTML = FinalHTML + ClusterName
    imagesLT = []
    FinalHTML = FinalHTML  # + "<div class=\"row\">"
    for i in ImageData:
        src = i[1]
        # F inalHTML = FinalHTML + "<div class=\"column\">" + "\n"
        imagesLT.append(r"<img src = " + "\"" + str(src) + "\" ALIGN=\"right\"/" + r">" + '\n\n')
        # print(ImageAdder)
        # FinalHTML = FinalHTML + ImageAdder
        # F inalHTML = FinalHTML + "</div>" + "\n"
    # FinalHTML = FinalHTML + "</div>" + "\n"

    PageText = ""
    for i in pageData:
        PageText = PageText + i[1]
    PageText = PageText.split(".")
    SentCount = 0
    ParCount = 0
    TextIns = ""
    NumImg = 0
    for i in PageText:

        if SentCount < 8:
            TextIns = TextIns + i + ". "
            SentCount += 1


        elif not (ParCount == 2):
            TextIns = TextIns + i + ". "
            SentCount += 1
            PGTex = r"<p>" + TextIns + r'</p><br>' + '\n\n'
            textq = "headline: " + PGTex[0:240].replace("<br>", "")
            max_len = 256
            encoding = tokenizer.encode_plus(textq, return_tensors="pt")
            input_ids = encoding["input_ids"].to(device)
            attention_masks = encoding["attention_mask"].to(device)
            beam_outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_masks,
                max_length=32,
                num_beams=2,
                early_stopping=True,
            )

            resultz = tokenizer.decode(beam_outputs[0])
            resultz = re.sub('<[^>]+>', '', resultz)
            resultz = resultz.replace("p>", "")
            resultz = resultz.strip("p>")
            FinalHTML = FinalHTML + "<h2>" + resultz + "</h2>\n"

            FinalHTML = FinalHTML + PGTex
            SentCount = 0
            ParCount += 1
            TextIns = ""
            if NumImg < 3:
                FinalHTML = FinalHTML + "\n" + imagesLT[NumImg] + "<br><br><br>"
                NumImg += 1

        else:
            openai.api_key = "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"
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt="What are 5 key points In the following paragraph: " + TextIns,
                temperature=0.3,
                max_tokens=320,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )

            logog = str(response)

            qweqw = logog[logog.find("text\"") + 10:logog.find("created\":") - 11]
            qweqw = qweqw.replace(r"\n", "<br>")

            PGTex = r"<p>" + qweqw + r'</p><br>' + '\n\n'

            textq = "headline: " + PGTex[0:240]

            max_len = 256

            encoding = tokenizer.encode_plus(textq, return_tensors="pt")
            input_ids = encoding["input_ids"].to(device)
            attention_masks = encoding["attention_mask"].to(device)

            beam_outputs = model.generate(
                input_ids=input_ids,
                attention_mask=attention_masks,
                max_length=32,
                num_beams=2,
                early_stopping=True,
            )

            resultz = tokenizer.decode(beam_outputs[0])
            resultz = re.sub('<[^>]+>', '', resultz)
            resultz = resultz.replace("p>", "")
            resultz = resultz.strip("p>")
            resultz = resultz.replace("<br", "")
            resultz = resultz.replace("br>", "")
            FinalHTML = FinalHTML + "<h2>" + resultz + "</h2>\n"

            FinalHTML = FinalHTML + PGTex
            SentCount = 0
            TextIns = ""
            ParCount += 1
            TextIns = ""

    for i in YouTubeData[0:3]:
        src = i[1]
        YoutIns = r"<iframe " + "width = \"420\" height = \"315\" src =" + "\"" + src + "\"" + r"></iframe>" + "\n\n"
        # print(ImageAdder)
        FinalHTML = FinalHTML + YoutIns

    for i in QandAData:
        FinalHTML = FinalHTML + "<h3>\n<strong>Question: " + i[1] + "</strong>\n</h3>\n"
        # FinalHTML = FinalHTML + r"<p>" + i[2] + r"</p><br>" + "\n"
        FinalHTML = FinalHTML + "<p>\n" + i[2] + "\n</p>\n<hr>"
        FinalHTML = FinalHTML + "\n\n"

    with open(r"QuestionINDSchema") as fs:
        Sch = fs.readlines()

    SchemaQ = ""
    for i in Sch:
        SchemaQ = SchemaQ + i

    AllScema = ""
    for i in QandAData:
        temps = SchemaQ
        name = i[1]
        # print(name)
        name = str.join(" ", name.splitlines())
        # name = name.replace("\n", "")
        anss = i[2]
        anss = str.join(" ", anss.splitlines()).replace("\"", "")
        NSS = "\"" + name + "\","
        temps = temps.replace("rdererss", NSS)
        temps = temps.replace("asdasdasdas", anss)
        AllScema = AllScema + temps
    print(AllScema)
    # AllScema = AllScema.rstrip(AllScema[-1])

    FinalHTML = FinalHTML.replace("dflkjensldjfasdkf", AllScema)
    FinalHTML = FinalHTML + "\n</body></html>"
    print(FinalHTML)
