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
from scipy.stats import poisson, skellam
import statsmodels.api as sm
import statsmodels.formula.api as smf
from time import sleep
from random import randint
from time import time
from warnings import warn
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import BeautifulSoup
from urllib2 import urlopen
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

w = []
LAP = []
LASHOnTarget = []
LASBlocked = []
LAKPass = []
LACross = []
LACorners = []
LAOffsides = []
LAInterceptions = []
LAGSaves = []
LAFouls = []
LHP = []
LHSTotal = []
LHSHOnTarget = []
LHSBloked = []
LHKPass = []
LHCross = []
LHCorners = []
LHOffsides = []
LHInterceptions = []
LHGSaves = []
LHFouls = []

data = []
Homes = []
AwayL = []
HomeL = []
HSL = []
ASL = []
ResultL = []
DateL = []
links = []


class Match(object):
    AP = 0
    ASHOnTarget = 0
    ASBlocked = 0
    AKPass = 0
    ACross = 0
    ACorners = 0
    AOffsides = 0
    AInterceptions = 0
    AGSaves = 0
    AFouls = 0
    HP = 0
    HSTotal = 0
    HSHOnTarget = 0
    HSBloked = 0
    HKPass = 0
    HCross = 0
    HCorners = 0
    HOffsides = 0
    HInterceptions = 0
    HGSaves = 0
    HFouls = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, AP, ASHOnTarget, ASBlocked, AKPass, ACross, ACorners, AOffsides, AInterceptions, AGSaves, AFouls,
                 HP, HSTotal, HSHOnTarget, HSBloked, HKPass, HCross, HCorners, HOffsides, HInterceptions,
                 HGSaves, HFouls):
        self.AP = AP
        self.ASHOnTarget = ASHOnTarget
        self.ASBlocked = ASBlocked
        self.AKPass = AKPass
        self.ACross = ACross
        self.ACorners = ACorners
        self.AOffsides = AOffsides
        self.AInterceptions = AInterceptions
        self.AGSaves = AGSaves
        self.AFouls = AFouls
        self.HP = HP
        self.HSTotal = HSTotal
        self.HSHOnTarget = HSHOnTarget
        self.HSBloked = HSBloked
        self.HKPass = HKPass
        self.HCross = HCross
        self.HCorners = HCorners
        self.HOffsides = HOffsides
        self.HInterceptions = HInterceptions
        self.HGSaves = HGSaves
        self.HFouls = HFouls




def make_result(AP, ASHOnTarget, ASBlocked, AKPass, ACross, ACorners, AOffsides, AInterceptions, AGSaves, AFouls,
                 HP, HSTotal, HSHOnTarget, HSBloked, HKPass, HCross, HCorners, HOffsides, HInterceptions,
                 HGSaves, HFouls):
    result = Match(AP, ASHOnTarget, ASBlocked, AKPass, ACross, ACorners, AOffsides, AInterceptions, AGSaves, AFouls,
                 HP, HSTotal, HSHOnTarget, HSBloked, HKPass, HCross, HCorners, HOffsides, HInterceptions,
                 HGSaves, HFouls)
    return result

mainURL = 'http://www.skysports.com/premier-league-results'

driver = webdriver.Chrome('C:\Users\Osama\Desktop\chromedriver.exe')
driver.get(mainURL)  # Get the playlist page
# Click the button
load_more_button = driver.find_element_by_class_name("plus-more")
load_more_button.click()

WebDriverWait(driver,10).until(EC.invisibility_of_element_located(
    (By.CLASS_NAME, "plus-more")))
# Get the html
html = driver.page_source
print(html)

def soup(URL):
    html_soup = bs(URL,"lxml")
    return html_soup


soup(html)


for u in soup(html).find_all('div', attrs={'class': 'fixres__item'}):
    tags = u.findAll('a', attrs={'class': 'matches__item matches__link'})
    for t in tags:
        link = t['href'].encode("utf8")
    links.append(link)
print(links)

statLinks = []
HeadDetailsL = []

def MStat(U):
     years = "17-18"
     cb = urlO(U)
     page = cb.read()
     soup = bs(page, "html.parser")
     time = soup.find('ul', attrs={'class': 'match-head__detail'}).find_all('li', attrs={'class': 'match-header__detail-item'})[1].text
     MatchTime = time[0:6]
     MatchDate = time[7:]
     Head = soup.findAll('a', attrs={'class': 'match-head__team-name'})
     Home = soup.findAll('abbr',attrs={'class': 'swap-text--bp10'})[0]['title']
     print(Home)
     HS = soup.find('span', attrs={'class': 'match-head__score'}).text.strip()
     Head2 = soup.findAll('a', attrs={'class': 'match-head__team-name'})
     Away = soup.findAll('abbr',attrs={'class': 'swap-text--bp10'})[1]['title']
     print Away
     AAS = soup.findAll('span', attrs={'class': 'match-head__score'})[1].text.strip()
     Result = 'D'
     if int(AAS) > int(HS):
         Result = 'A'
     elif int(AAS) < int(HS):
         Result = 'H'
     else:
         Result = 'D'
     HeadDetails = soup.findAll("ul", {"class": "match - head__detail"})
     for HeadDetail in HeadDetails:
         HeadDetailn = HeadDetail.findAll('li',attrs={"class": "match-header__detail-item"}).text
         HeadDetailsL.append(HeadDetailn)
     print(HeadDetailsL)
     All = soup.findAll("span", {"class": "match-stats__bar"})
     for i in All:
         i = soup.findAll(attrs={"class": "match-stats__away"})
         data = [ele.text.strip().encode("utf8").replace('away\n', '') for ele in i]
     #  Data.append([ele for ele in int if ele])
     AP = data[0]
     ASTotal = data[1]
     ASHOnTarget = data[2]
     ASBlocked = data[4]
     AKPass = data[7]
     ACross = data[9]
     ACorners = data[12]
     AOffsides = data[13]
     AInterceptions = data[15]
     AGSaves = data[21]
     AFouls = data[23]

     for i in All:
         i = soup.findAll(attrs={"class": "match-stats__home"})
         Homes = [ele.text.strip().encode("utf8").replace('home\n', '') for ele in i]
     # Data.append([ele for ele in str if ele])
     HP = Homes[0]
     HSTotal = Homes[1]
     HSHOnTarget = Homes[2]
     HSBloked = Homes[4]
     HKPass = Homes[7]
     HCross = Homes[9]
     HCorners = Homes[12]
     HOffsides = Homes[13]
     HInterceptions = Homes[15]
     HGSaves = Homes[21]
     HFouls = Homes[23]

     make_result(AP, ASHOnTarget, ASBlocked, AKPass, ACross, ACorners, AOffsides, AInterceptions, AGSaves, AFouls,
                 HP, HSTotal, HSHOnTarget, HSBloked, HKPass, HCross, HCorners, HOffsides, HInterceptions,
                 HGSaves, HFouls)

     for HS in HSL:
         print(HS)



     sql(AP,
         ASTotal,
         ASHOnTarget,
         ASBlocked,
         AKPass,
         ACross,
         ACorners,
         AOffsides,
         AInterceptions,
         AGSaves,
         AFouls,
         Away,
         AAS,
         Result,
         HS,
         Home,
         HP,
         HSTotal,
         HSHOnTarget,
         HSBloked,
         HKPass,
         HCross,
         HCorners,
         HOffsides,
         HInterceptions,
         HGSaves,
         HFouls,
         MatchTime,
         MatchDate,
         years)




def sql(AP,
        ASTotal,
        ASHOnTarget,
        ASBlocked,
        AKPass,
        ACross,
        ACorners,
        AOffsides,
        AInterceptions,
        AGSaves,
        AFouls,
        Away,
        AAS,
        Result,
        HS,
        Home,
        HP,
        HSTotal,
        HSHOnTarget,
        HSBloked,
        HKPass,
        HCross,
        HCorners,
        HOffsides,
        HInterceptions,
        HGSaves,
        HFouls,
        MatchTime,
        MatchDate,
        years):
    query = """REPLACE INTO RESULTS (
    AP                ,
    ASTotal           ,
    ASHOnTarget       ,
    ASBlocked         ,
    AKPass            ,
    ACross            ,
    ACorners          ,
    AOffsides         ,
    AInterceptions    ,
    AGSaves           ,
    AFouls            ,
    Away              ,
    AAS               ,
    Result            ,
    HS                ,
    Home              ,
    HP                ,
    HSTotal           ,
    HSHOnTarget       ,
    HSBloked          ,
    HKPass            ,
    HCross            ,
    HCorners          ,
    HOffsides         ,
    HInterceptions    ,
    HGSaves           ,
    HFouls            ,
    MatchTime         ,
    MatchDate         ,
    years      
    )  
    VALUES(%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s);"""
    data = (str(AP),
            str(ASTotal),
            str(ASHOnTarget),
            str(ASBlocked),
            str(AKPass),
            str(ACross),
            str(ACorners),
            str(AOffsides),
            str(AInterceptions),
            str(AGSaves),
            str(AFouls),
            str(Away),
            str(AAS),
            str(Result),
            str(HS),
            str(Home),
            str(HP),
            str(HSTotal),
            str(HSHOnTarget),
            str(HSBloked),
            str(HKPass),
            str(HCross),
            str(HCorners),
            str(HOffsides),
            str(HInterceptions),
            str(HGSaves),
            str(HFouls),
            str(MatchTime),
            str(MatchDate),
            str(years)
            )
    cursor.execute(query, data)
    cnx.commit()


# def Delete(T):
#    bool(T)
#    if T is True:
#        qry = "DROP TABLE IF EXISTS results"
#        cursor.execute(qry)
#        sql1 = """CREATE TABLE results (
#      RID            INT(11) ,
#      AP             varchar(45) ,
#      ASTotal        varchar(45) ,
#      ASHOnTarget    varchar(45) ,
#      ASBlocked      varchar(45) ,
#      AKPass         varchar(45) ,
#      ACross         varchar(45) ,
#      ACorners       varchar(45) ,
#      AOffsides      VARCHAR(45) ,
#      AInterceptions varchar(45) ,
#      AGSaves        varchar(45) ,
#      AFouls         varchar(45) ,
#      Away           varchar(45) ,
#      AAS            varchar(45) ,
#      Result         varchar(6) ,
#      HS             varchar(45) ,
#      Home           varchar(45) ,
#      HP             varchar(45) ,
#      HSTotal        varchar(45) ,
#      HSHOnTarget    varchar(45) ,
#      HSBloked       VARCHAR(45) ,
#      HKPass         varchar(45) ,
#      HCross         varchar(45) ,
#      HCorners       varchar(45) ,
#      HOffsides      varchar(45) ,
#      HInterceptions varchar(45) ,
#      HGSaves        varchar(45) ,
#      HFouls         VARCHAR(45)
#
#
#    )"""
#        cursor.execute(sql1)
#
#
# m = True
# Delete(m)


def stat(AP,
         ASHOnTarget,
         ASBlocked,
         AKPass,
         ACross,
         ACorners,
         AOffsides,
         AInterceptions,
         AGSaves,
         AFouls,
         HP,
         HSTotal,
         HSHOnTarget,
         HSBloked,
         HKPass,
         HCross,
         HCorners,
         HOffsides,
         HInterceptions,
         HGSaves,
         HFouls,
         AwayL,
         HomeL,
         HSL,
         ASL,
         ResultL
         ):
    test_df = pd.DataFrame({'Home': HomeL,
                            'HS': HSL,
                            'AS': ASL,
                            'Away': AwayL,
                            'Results': ResultL,
                            'HP': LHP,
                            'AP': LAP,
                            'HSTotal': LHSTotal,
                            # 'ASTotal': ASTotal
                            'HSHOnTarget': LHSHOnTarget,
                            'ASHOffTarget': LASHOnTarget,
                            'HSBloked': LHSBloked,
                            'ASBlocked': LASBlocked,
                            'HKPass': LHKPass,
                            'AKPass': LAKPass,
                            'HCross': LHCross,
                            'ACross': LACross,
                            'HCorners': LHCorners,
                            'ACorners': LACorners,
                            'HOffsides': LHOffsides,
                            'AOffsides': LAOffsides,
                            'HInterceptions': LHInterceptions,
                            'AInterceptions': LAInterceptions,
                            'HGSaves': LHGSaves,
                            'AGSaves': LAGSaves,
                            'HFouls': LHFouls,
                            'AFouls': LAFouls
                            })

    print test_df

    engine = create_engine("mysql://admin:admin@localhost/football")
    test_df.to_sql(name='plr', con=engine, schema='football', if_exists='replace')


kaka = []
links = [i for i in links if i != '']

def main():
    s = []
    for linkr in links:
        cb = urlO(linkr)
        page = cb.read()
        html_soup = bs(page, "html.parser")
        u4 = html_soup.find('ul', attrs={'class': 'page-nav__item-group'}). \
            find_all('li', attrs={'class': 'page-nav__item'})[8].find('a', attrs={'class': 'page-nav__link'})\
            ['href'].replace('http://www.skybet.com/go/class/5/type/1?aff=1010', '').encode("utf8")
        s = [i for i in s if i != '']
        s.append(u4)
    print(s)
    for l in s:
        MStat(l)

main()
    # for hs in HSL:
    #     for h in HomeL:
    #         for r in ResultL:
    #             for a in AwayL:
    #                 for ass in ASL:
    #                     k.append(a)
    #                     k.append(ass)
    #                     k.append(r)
    #                     k.append(hs)
    #                     k.append(h)

# for c in s:
#    so = plr()
#    print so
#    k = MStat(c,so)
#
#    #
# stat(LAP,
#     LASHOnTarget,
#     LASBlocked,
#     LAKPass,
#     LACross,
#     LACorners,
#     LAOffsides,
#     LAInterceptions,
#     LAGSaves,
#     LAFouls,
#     LHP,
#     LHSTotal,
#     LHSHOnTarget,
#     LHSBloked,
#     LHKPass,
#     LHCross,
#     LHCorners,
#     LHOffsides,
#     LHInterceptions,
#     LHGSaves,
#     LHFouls,
#     AwayL,
#     HomeL,
#     HSL,
#     ASL,
#     ResultL
#     )
# print(kaka)

# kaka.append(AP)
# kaka.append(HP)
# kaka.append(ASHOnTarget)
# kaka.append(HSHOnTarget)
# kaka.append(ASBlocked)
# kaka.append(HSBloked)
# kaka.append(AKPass)
# kaka.append(HKPass)
# kaka.append(ACross)
# kaka.append(HCross)
# kaka.append(ACorners)
# kaka.append(HCorners)
# kaka.append(AOffsides)
# kaka.append(HOffsides)
# kaka.append(AInterceptions)
# kaka.append(HInterceptions)
# kaka.append(AGSaves)
# kaka.append(HGSaves)
# kaka.append(AFouls)
# kaka.append(HFouls)
# kaka.append(HSTotal)
# print(kaka)
# return kaka
# kaka = []
# global AP
# global ASHOnTarget
# global ASBlocked
# global AKPass
# global ACross
# global ACorners
# global AOffsides
# global AInterceptions
# global AGSaves
# global AFouls
# global HP
# global HSTotal
# global HSHOnTarget
# global HSBloked
# global HKPass
# global HCross
# global HCorners
# global HOffsides
# global HInterceptions
# global HGSaves
# global HFouls
# AP.append(k[0])
#       LASHOnTarget.append(k[1])
#       LASBlocked.append(k[2])
#       LAKPass.append(k[3])
#       LACross.append(k[4])
#       LACorners.append(k[5])
#       LAOffsides.append(k[6])
#       LAInterceptions.append(k[7])
#       LAGSaves.append(k[8])
#       print(LAGSaves)
#       LAFouls.append(k[9])
#       LHP.append(k[10])
#       LHSTotal.append(k[11])
#       LHSHOnTarget.append(k[12])
#       LHSBloked.append(k[13])
#       LHKPass.append(k[14])
#       LHCross.append(k[15])
#       LHCorners.append(k[16])
#       LHOffsides.append(k[17])
#       LHInterceptions.append(k[18])
#       LHGSaves.append(k[19])
#       LHFouls.append(k[20])
