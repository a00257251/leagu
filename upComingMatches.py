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


def sql(Away,
        MatchTime,
        MatchDate,
        Home

):
    query = """INSERT INTO upcoming (
      Away              ,
      MatchTime         , 
      MatchDate         , 
      Home              
    )  
    VALUES(%s, %s, %s,%s) 
     ;"""
    data = (
        str(Away),
        str(MatchTime),
        str(MatchDate),
        str(Home)
    )
    cursor.execute(query, data)
    cnx.commit()


def UPLR():
    my_url = "http://www.skysports.com/premier-league-fixtures"
    cb = urlO(my_url)
    page = cb.read()
    html_soup = bs(page, "html.parser")
    AwayL = []
    HomeL = []
    HSL = []
    DateL = []

    TeamHome = html_soup.find('div', attrs={'class': 'fixres__body'})
    Date2 = TeamHome.findAll('a', attrs={'class': 'matches__item matches__link'})
    Date1 = TeamHome.findAll('h4', attrs={'class': 'fixres__header2'})
    for time in Date1:
        if time.text == time.text:
            MatchDate = time.text
            print MatchDate
            DateL.append(MatchDate)
            for time in Date2:
                Home1 = time.findAll('span',
                                     attrs={'class': 'matches__item-col matches__participant matches__participant--side1'})
                for i in Home1:
                    Home = i.text.strip()
                    Home = str(Home)
                    DateL.append(Home)
                    HomeScore = time.findAll('span', attrs={'class': 'matches__date'})
                    for i in HomeScore:
                        MatchTime = i.text.strip()
                        print MatchTime
                        DateL.append(MatchTime)
                        Away1 = time.findAll('span', attrs={
                            'class': 'matches__item-col matches__participant matches__participant--side2'})
                        for i in Away1:
                            Away = i.text.strip()
                            Away = str(Away)
                            DateL.append(Away)

                            sql(Away, MatchTime, MatchDate, Home)




UPLR()
