import pymysql
import pandas as pd
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
from scrapy import cmdline
from sqlalchemy import create_engine

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




def df():
    cursor.execute(' SELECT * FROM burnley ')
    table_rows2 = cursor.fetchall()
    df1 = pd.DataFrame(table_rows2)
    df1 = pd.read_sql('SELECT * FROM burnley', cnx)
    df1['AS'] = df1.AS.astype(int)
    df1['HS'] = df1.HS.astype(int)
    df1['Results'] = df1.Results.astype(str)


def df1():
    cursor.execute(' SELECT * FROM mancitymatches ')
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows)
    df = pd.read_sql('SELECT * FROM mancitymatches', cnx)
    df['AS'] = df.AS.astype(int)
    AS = df['AS']
    df['HS'] = df.HS.astype(int)
    HS = df['HS']
    df['Results'] = df.Results.astype(str)

print(df)
upsets = 0
non_upsets = 0


starting_bankroll = 100
wagering_size = 5

bankroll = starting_bankroll
#def t(g):
 #   for f in g:
      # print(g)
#t(HS)
#t(AS)


def get_last_matches(team,team2,R):
    cursor.execute(' SELECT * FROM burnley ')
    table_rows2 = cursor.fetchall()
    df1 = pd.DataFrame(table_rows2)
    df1 = pd.read_sql('SELECT * FROM burnley', cnx)
    df1['AS'] = df1.AS.astype(int)
    df1['HS'] = df1.HS.astype(int)
    df1['Results'] = df1.Results.astype(str)

    cursor.execute(' SELECT * FROM mancitymatches ')
    table_rows = cursor.fetchall()
    df = pd.DataFrame(table_rows)
    df = pd.read_sql('SELECT * FROM mancitymatches', cnx)
    df['AS'] = df.AS.astype(int)
    AS = df['AS']
    df['HS'] = df.HS.astype(int)
    HS = df['HS']
    df['Results'] = df.Results.astype(str)

    t_matches = df[(df['Home'] == team) & (df['Results'] == R)]
    p_matches = len(df[(df['Home'] == team) & (df['Results'] == R)])
    f_matches = df1[(df1['Home'] == team2) & (df1['Results'] == R)]
    p2_matches = len(df1[(df1['Home'] == team2) & (df1['Results'] == R)])
    r = pd.concat([t_matches , f_matches])
    p = (p_matches , p2_matches)
    if p_matches > p2_matches:
        return team + ' will win'
    elif  p_matches < p2_matches:
        return team2 + ' will win '
    else:
        return  ' Drow '

l = get_last_matches('Liverpool FC','Burnley','H')

print(l)





#
# #df['Team'] = df.Team.astype(str)
# #df['PlayerName'] = df.PlayerName.astype(str)
# df['AS']
# print(df)
# print df.dtypes
# print df.describe()
# print df['Results'].max
# fig = plt.figure(figsize=(12, 6))
# AS = fig.add_subplot(121)
# HS = fig.add_subplot(122)
#
# AS.hist(df.AS, bins=80)
# AS.set_xlabel('F')
# AS.set_title("AWAY GOALS")
#
# HS.hist(df.HS, bins=80)
# HS.set_xlabel(' Yollow Cards ')
# HS.set_title("HOME GOALS")
# bh =len(df1[df1.Home =='Burnley'])
# lh =len(df[df.Home =='Liverpool FC'])
# print(bh)
# print(lh)
#
# def get_result_stats(playing_stats):
#     return pd.DataFrame(data = [ len(playing_stats[playing_stats.Results == 'H']),
#                                  len(playing_stats[playing_stats.Results == 'A']),
#                                   len(playing_stats[playing_stats.Results == 'D'])],
#                         index = ['Home Wins', 'Away Wins', 'Draws'],
#                         columns = ['Liver']
#                                   ).T
# r1 = get_result_stats(df)
# r2 = get_result_stats(df1)
# print(r1)
# f = pd.concat([r1,r2])
#
# print(f)
#
#
# def getall_h2h_record(team):
#     df_dict = {}
#     for some_team in teams:
#         stat = h2h_stats[team][some_team]
#         res = h2hc[team][some_team]
#         stat[res[0][0]] = res[0][1]
#         stat[res[1][0]] = res[1][1]
#         df_dict[some_team] = stat
#     df = pd.DataFrame(data=df_dict).T
#
#     # Rename columns for h2hc_year
#
#     # Reorder columns
#     df.fillna(value='None')
#     cols = [team + ' Home Wins', 'Home Losses', 'Home Draws', 'Home Result of ',
#             team + ' Away Wins', 'Away Losses', 'Away Draws', 'Total Matches', 'Away Result of ']
#     df = df[cols]
#     return df
#
# h2h14_mancity = getall_h2h_record('Liverpool FC')
#
# def get_h2h_prob(h2h14, team, num_matches):
#     cols = [team +' Home Wins', 'Home Losses', 'Home Draws', team + ' Away Wins', 'Away Losses', 'Away Draws']
#     for column in cols:
#         h2h14[column] = h2h14[column] / (num_matches/2)
#     return h2h14
#
# get_h2h_prob(h2h14_mancity, 'Man City', 10)
#
#
# while bh is not None:
#     bh =(len(df1[df1.Results =='H']))
#     break
# ba = (df1[df1.Away == 'Burnley'])
# while ba is not None:
#     Ab = (len(df1[df1.Results == 'A']))
#     break
#
# live2 = Ab + bh
# c1 = (float(live2) / 50) * 100
# print(c1)
#
# while lh is not None:
#     h =(len(df[df.Results =='H']))
#     break
# la = len(df[df.Away == 'Liverpool FC'])
# while la is not None:
#     A = (len(df[df.Results == 'A']))
#     break
#
# live = A + h
# c = (float(live) / 50) * 100
# print(c)
#
#



#
#
#
#
# n_homewins = len(df[df.Results == 'H'])
# n_Awaywins = len(df[df.Results == 'A'])
# win_rate = (float(n_homewins) / (n_Awaywins)) * 100
# print win_rate
# print(n_homewins)
# print(n_Awaywins)
# print plt.show()
#
# clf = svm.SVC()
#
#
# m = ols('AS ~ HS',df).fit()
# print (m.summary())
#
# m = ols('AS ~ HS + Results',df).fit()
# print (m.summary())
#
#
# sns.jointplot(x="AS", y="HS", data=df, kind = 'reg',fit_reg= True, size = 7)
# plt.show()
#
# dfY = df['AS']
# dfR = df['HS']
# #print dfM.mean()
#
# print skellam.pmf(0.0,  df.mean()[1],  df.mean()[2])
# print skellam.pmf(1,  df.mean()[1],  df.mean()[2])
#
#
#
#
#
# goal_model_data = pd.concat([df[['Home','Away','HS']].assign(home=1).rename(
#             columns={'HomeTeam':'team', 'AwayTeam':'opponent','HomeGoals':'goals'}),
#           df[['Away','Home','AS']].assign(home=0).rename(
#             columns={'AwayTeam':'team', 'HomeTeam':'opponent','AwayGoals':'goals'})])
#
#
# poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
#                         family=sm.families.Poisson()).fit()
# poisson_model.summary()