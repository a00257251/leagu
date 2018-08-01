import pymysql
import pandas as pd
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from scrapy import cmdline
from sqlalchemy import create_engine
import MySQLdb
import ast
import scrapy
from scrapy.cmdline import execute
from urllib2 import urlopen as urlO
from bs4 import BeautifulSoup as bs
import csv
import datetime
from pymongo import MongoClient
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import seaborn as sns
from matplotlib import rcParams
from sklearn import svm
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf

try:
    cnx = mysql.connector.connect(user='admin',
                                  password='admin',
                                  database='football')
    cursor = cnx.cursor()
except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("you are connected")

#cursor.execute('SELECT * FROM Arsenal')
#table_rows = cursor.fetchall()
#df = pd.DataFrame(table_rows)
#df = pd.read_sql('SELECT * FROM Arsenal', cnx)
#
#df['PLD'] = df.PLD.astype(int)
#df['G'] = df.G.astype(int)
#df['YC'] = df.YC.astype(int)
#df['RC'] = df.RC.astype(int)
#df['FF'] = df.FF.astype(int)
##df['Team'] = df.Team.astype(str)
##df['PlayerName'] = df.PlayerName.astype(str)
#df['PLD']
#print(df['PLD'])
#print df.dtypes
#print df.describe()
#
#fig = plt.figure(figsize=(12, 6))
#G = fig.add_subplot(121)
#YC = fig.add_subplot(122)
#
#G.hist(df.G, bins=80)
#G.set_xlabel('F')
#G.set_title("Histogram of Number of Goals")
#
#YC.hist(df.YC, bins=80)
#YC.set_xlabel(' Yollow Cards ')
#YC.set_title("Histogram of Yollow Cards ")
#
#print plt.show()
#
#clf = svm.SVC()
#
#
#m = ols('G ~ YC',df).fit()
#print (m.summary())
#
#m = ols('G ~ YC + RC + FF ',df).fit()
#print (m.summary())
#
#
#sns.jointplot(x="G", y="YC", data=df, kind = 'reg',fit_reg= True, size = 7)
#plt.show()
#
#dfY = df['YC']
#dfR = df['RC']
##print dfM.mean()
#
#print skellam.pmf(0.0,  df.mean()[1],  df.mean()[2])
#print skellam.pmf(1,  df.mean()[1],  df.mean()[2])
#
#
#
#
#
#goal_model_data = pd.concat([df[['HomeTeam','AwayTeam','HomeGoals']].assign(home=1).rename(
#            columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
#          df[['AwayTeam','HomeTeam','AwayGoals']].assign(home=0).rename(
#            columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])
#
#
##
## db = MySQLdb.connect("localhost","admin","admin","football" )
##
## # prepare a cursor object using cursor() method
## cursor = db.cursor()
##
## # Drop table if it already exist using execute() method.
## cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
##
## # Create table as per requirement
## sql = """CREATE TABLE EMPLOYEE (
##          FIRST_NAME  CHAR(20) NOT NULL,
##          LAST_NAME  CHAR(20),
##          AGE INT,
##          SEX CHAR(1),
##          INCOME FLOAT )"""
##
## cursor.execute(sql)
##
## # disconnect from server
##
## # Prepare SQL query to INSERT a record into the database.
## sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
##          LAST_NAME, AGE, SEX, INCOME)
##          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
## try:
##    # Execute the SQL command
##    cursor.execute(sql)
##    # Commit your changes in the database
##    db.commit()
## except:
##    # Rollback in case there is any error
##    db.rollback()
##
## # disconnect from server
##
## # Using the cursor as iterator
## cursor.execute("SELECT last_insert_id();")
## for row in cursor:
##
##     print(row)
##
## sql = "SELECT * FROM PLAYER \
##        WHERE PLAYERID = 42"
## try:
##    # Execute the SQL command
##    cursor.execute(sql)
##    # Fetch all the rows in a list of lists.
##    results = cursor.fetchone()
##    for row in results:
##       fname = int(row[0])
##       lname = row[1]
##       age = row[2]
##       sex = row[3]
##       income = row[4]
##       incomeT = row[5]
##       incomeT2 = row[6]
##       #Now print fetched resul
##       print(results)
##
##except:
##   print "Error: unable to fecth data"
#
## disconnect from server
#sql = "SELECT * FROM player WHERE id == '%d'" % (2)
#try:
#   # Execute the SQL command
#   cursor.execute(sql)
#   # Fetch all the rows in a list of lists.
#   results = cursor.fetchall()
#   for cols in results:
#
#      PLD = cols[1]
#      G = cols[2]
#      YC = cols[3]
#      RC = cols[4]
#      FF = cols[5]
#      fd = cols[6]
#     # Now print fetched result
#      print "PLD=%s,G=%d,YC=%s,RC=%d,FF=%s,fd=%s" % \
#            (PLD, G, YC, RC,  FF, fd)
#
#except:
#    print "Error: unable to fecth data"
#




def Delete(T):
    bool(T)
    if  T is True :



      sql1 = """CREATE TABLE Player (
      PlayerName varchar(45) NOT NULL,
      PLD varchar(45) DEFAULT NULL,
      G varchar(45) DEFAULT NULL,
      YC varchar(45) DEFAULT NULL,
      RC varchar(45) DEFAULT NULL,
      FF varchar(45) DEFAULT NULL,
      Team VARCHAR(45)


    )"""

    cursor.execute(sql1)



def PlayerSearch(tableClass,index):
    Team = html_soup.find('span', attrs={'class' : 'swap-text__target'}).text
    print(Team)
    table = html_soup.findAll('table', attrs={'class': tableClass})[int(index)].find_all('tr')[1:]
    for row in table:
      cols = row.findChildren(recursive=False)
      cols = [ele.text.strip().encode("utf8") for ele in cols]
      if cols:
         PlayerName = cols[0]
         PLD = str(cols[1])
         G = str(cols[2])
         YC = str(cols[3])
         RC = str(cols[4])
         FF = str(cols[5])

         sql(PlayerName, PLD, G, YC, RC, FF, Team)


def sql(PlayerName, PLD, G, YC, RC, FF, Team):
    TeamTableName = html_soup.find('span', attrs={'class': 'swap-text__target'}).text.replace(' ', '')
    cursor = cnx.cursor()
    sql = "INSERT INTO Player (PlayerName, PLD, G, YC, RC, FF, Team) VALUES (%s, %s, %s, %s, %s, %s, %s);"
    data = (str(PlayerName).replace('-','0'), str(PLD)[0:2].replace('-','0'), str(G).replace('-','0'),
            str(YC).replace('-','0'),str(RC).replace('-','0'), str(FF).replace('-','0'),str(Team))
    cursor.execute(sql,data)
    print(str(PlayerName), str(PLD),str(G), str(YC),str(RC), str(FF),str(Team))
    cnx.commit()



my_url = "http://www.skysports.com/bournemouth"
cb = urlO(my_url)
page = cb.read()
html_soup = bs(page, "html.parser")
f = html_soup.find('optgroup')
TeamTableName = f.find_all('option')
for o in TeamTableName:
    x = o['value']
    print(x)
    my_url = "http://www.skysports.com{}-stats".format(x)
    cb = urlO(my_url)
    page = cb.read()
    html_soup = bs(page, "html.parser")
    tableClass = 'table -small no-wrap football-squad-table '
    T = True
    #Delete(T)
    i = 0
    for i in range(0, 4):
        PlayerSearch(tableClass, i)
        i = i + 1



# my_url = "http://www.skysports.com/premier-league-fixtures"
# cb = urlO(my_url)
# page = cb.read()
# html_soup = bs(page, "html.parser")
# table = html_soup.find('div', attrs={'class': 'fixres__body'}).find_all('span')
# for row in table:
#     cols = row.findChildren(recursive=False)
#     cols = [ele.text.strip().encode("utf8") for ele in cols]
#     if cols:
#         PlayerName = [cols]
#         print(PlayerName)
#
# f = html_soup.find('div')
# k = f.find('fixres__body')
# TeamTableName = k.findAll('fixres__item')
# for o in TeamTableName:
#     row = o.findAll()
#     print(x)
#     my_url = "http://www.skysports.com{}-stats".format(x)
#     cb = urlO(my_url)
#     page = cb.read()
#     html_soup = bs(page, "html.parser")
#     tableClass = 'table -small no-wrap football-squad-table '
#     T = True
#     Delete(T)
#     i = 0
#     for i in range(0, 4):
#         PlayerSearch(tableClass, i)
#         i = i + 1
#




