from aifc import Error
from datetime import time
import time
# import NewsGet
import mysql.connector


import QandARet
import GoogleImage
import QandARet
import TextFromWebGet
import YouTube


vidURLS = YouTube.getYout.URLs
ImgURLS = GoogleImage.getGoogImage.FinImg
ans = QandARet.getQandA.finAns
que = QandARet.getQandA.finQuest
print(ans)
print(que)
ClusterIDOfSubject = 1
TextFromSites = TextFromWebGet.webCont.TextFromsites
print(TextFromSites)

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

        for i in range(0, len(ans)):
            time.sleep(0.5)
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO qandout(ClusterID, Question, Answer)
            VALUES (%s,%s,%s)"""
            insert_tuple_1 = (ClusterIDOfSubject, que[i], ans[i])
            cursor.execute(sql_insert_query, insert_tuple_1)
            connection.commit()


        for i in range(0, len(vidURLS)):
            time.sleep(0.5)
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO youtubevids(ClusterID, URLOfVid)
                        VALUES (%s,%s)"""
            insert_tuple_1 = (int(ClusterIDOfSubject), str(vidURLS[i]))
            cursor.execute(sql_insert_query, insert_tuple_1)
            connection.commit()

        for i in range(0, len(ImgURLS)):
            time.sleep(0.5)
            cursor = connection.cursor()
            sql_insert_query = """INSERT INTO images(ClusterID, URLOfImage)
                               VALUES (%s,%s)"""
            insert_tuple_1 = (int(ClusterIDOfSubject), str(ImgURLS[i]))
            cursor.execute(sql_insert_query, insert_tuple_1)
            connection.commit()


        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO pagetext(ClusterID, Text)
                                       VALUES (%s,%s)"""
        insert_tuple_1 = (ClusterIDOfSubject, TextFromSites)
        cursor.execute(sql_insert_query, insert_tuple_1)
        connection.commit()
        '''
        cursor = connection.cursor()
        sql_insert_query = """INSERT INTO newstext(ClusterID, NewsText)
                                       VALUES (%s,%s)"""
        insert_tuple_1 = (ClusterIDOfSubject, NewsTex)
        cursor.execute(sql_insert_query, insert_tuple_1)
        '''
        connection.commit()


        print("Table connected successfully")

except Error as e:
    print("Error while connecting to MySQL", e)





import HTMLFromDB
HTMLFromDB.MakePage()
