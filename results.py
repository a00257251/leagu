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

def PLR():
    my_url = "http://www.skysports.com/premier-league-results"
    cb = urlO(my_url)
    page = cb.read()
    html_soup = bs(page, "html.parser")
    AwayL = []
    HomeL = []
    HSL = []
    ASL = []
    ResultL = []
    DateL =[]
    TeamHome = html_soup.find('div', attrs={'class': 'fixres__body'})
    Date2 = TeamHome.findAll('a', attrs={'class': 'matches__item matches__link'})
    Date1 = TeamHome.findAll('h4', attrs={'class': 'fixres__header2'})
    for time in Date1:
        Date = time.text
        DateL.append(Date)
    for time in Date2:
        Home1 = time.findAll('span',attrs={'class': 'matches__item-col matches__participant matches__participant--side1'})
        for i in Home1:
            Home = i.text.strip()
            HomeL.append(Home)
        HomeScore= time.findAll('span',attrs={'class': 'matches__teamscores-side'})[0]
        for i in HomeScore:
            HS = int(i)
            HSL.append(HS)
        AwayScore=time.findAll('span',attrs={'class': 'matches__teamscores-side'})[1]
        for i in AwayScore:
            AS = int(i)
            ASL.append(AS)
        Away1 = time.findAll('span', attrs={'class': 'matches__item-col matches__participant matches__participant--side2'})
        for i in Away1:
            Away = i.text.strip()
            AwayL.append(Away)
        Result = 'D'
        for i in HSL:
            H = i
        for i in ASL:
            if i > H:
                Result = 'A'
            elif i < H:
                Result = 'H'
            else:
                Result = 'D'
        ResultL.append(Result)


        test_df = pd.DataFrame({'Home': HomeL,
                                    'HS': HSL,
                                    'AAS': ASL,
                                    'Away': AwayL,
                                    'Results': ResultL
                                    })
    engine = create_engine("mysql://admin:admin@localhost/football")
    test_df.to_sql(name='PLR',con=engine,schema='football',if_exists='replace')

