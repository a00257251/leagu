import pydotplus
from sklearn import tree
from IPython.display import Image, display
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn
from scipy.stats import poisson,skellam
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
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.model_selection import train_test_split
import random
from sklearn import model_selection
import numpy
from sklearn.cross_validation import train_test_split
from pandas.plotting import scatter_matrix
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn import linear_model
from sklearn.svm import SVC
import scipy.sparse as sp
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from random import sample
from sklearn.linear_model import LogisticRegression
from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.cross_validation import cross_val_score
from sklearn import metrics
from IPython.display import Image
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as smf
import warnings
import seaborn as sns
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import SGDClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn import tree
import matplotlib.pyplot as plt
warnings.simplefilter("ignore")
from sklearn import preprocessing


connection = connection.MySQLConnection(user='admin', password='admin',
                                        host='localhost',
                                        database='football')
cursor = connection.cursor()

try:
    cnx = mysql.connector.connect(user='admin',
                                  password='admin',
                                  database='football')
except mysql.connector.Error as err:

    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print("you are connected")



df = pd.read_sql('''SELECT Home,Away,AP,AAS,HS,Result FROM results ''',cnx)
data = pd.read_sql('''SELECT * FROM results ''',cnx)

print data

data['AP'] = data.AP.astype(float)
data['ASTotal'] = data.ASTotal.astype(float)
data['ASHOnTarget'] = data.ASHOnTarget.astype(float)
data['ASBlocked'] = data.ASBlocked.astype(float)
data['AKPass'] = data.AKPass.astype(float)
data['ACross'] = data.ACross.astype(float)
data['ACorners'] = data.AAS.astype(float)
data['AOffsides'] = data.HS.astype(float)
data['HSTotal'] = data.HSTotal.astype(float)
data['HSHOnTarget'] = data.HSHOnTarget.astype(float)
data['HSBloked'] = data.AP.astype(float)
data['HKPass'] = data.ASTotal.astype(float)
data['HCross'] = data.ASHOnTarget.astype(float)
data['HCorners'] = data.ASBlocked.astype(float)
data['HInterceptions'] = data.AKPass.astype(float)
data['HP'] = data.HP.astype(float)
data['AAS'] = data.AAS.astype(float)
data['HS'] = data.HS.astype(float)
data['Result'] = data.Result.astype(str)




df['AAS'] = df.AAS.astype(float)
df['HS'] = df.HS.astype(float)
df['Result'] = df.Result.astype(str)
#print df.mean()
#print skellam.pmf(0.0,  df.mean()[0],  df.mean()[1])
#print skellam.pmf(1,  df.mean()[0],  df.mean()[1])


goal_model_data = pd.concat([data[['Home','Away','HS','HP','HKPass','HSHOnTarget']].assign(home=1).rename(
          columns={'Home':'team','HP':'P','HKPass':'KPass','HSHOnTarget':'SHOnTarget','Away':'opponent','HS':'goals'}),
          data[['Away','Home','AAS','AP','AKPass','ASHOnTarget']].assign(home=0).rename(
          columns={'Away':'team', 'AP':'P','AKPass':'KPass','ASHOnTarget':'SHOnTarget','Home':'opponent','AAS':'goals'})])

#print(goal_model_data)
#poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
 #                       family=sm.families.Poisson()).fit()
#print poisson_model.summary()

#print poisson_model.predict(pd.DataFrame(data={'team': 'Chelsea', 'opponent': 'Manchester City',
#                                       'home':0},index=[1]))

#print poisson_model.predict(pd.DataFrame(data={'team': 'Manchester City', 'opponent': 'Chelsea',
#                                       'home':0},index=[1]))



def simulate_match(homeTeam, awayTeam, max_goals=10):

    poisson_model = smf.glm(formula="goals ~SHOnTarget+ P + home + team + opponent", data=goal_model_data,
                            family=sm.families.Poisson()).fit() #5.33333391412 # 5.7457 8982881

    home_goals_avg = poisson_model.predict(pd.DataFrame(data={'SHOnTarget': data.HSHOnTarget,'P': data.HP, 'team': homeTeam,'opponent': awayTeam, 'home':1},index=[9])).values[0]
    print(home_goals_avg)
    away_goals_avg = poisson_model.predict(pd.DataFrame(data={'SHOnTarget': data.ASHOnTarget,'P': data.AP, 'team': awayTeam,'opponent': homeTeam,'home':0},index=[1])).values[0]
    print(away_goals_avg)
    team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals+1)] for team_avg in [home_goals_avg, away_goals_avg]]

    return(np.outer(np.array(team_pred[0]), np.array(team_pred[1])))

#print simulate_match('Swansea City', 'Bournemouth', max_goals=3)

#chel_sun = simulate_match('Bournemouth', 'Liverpool', max_goals=10)

#print chel_sun

#print np.sum(np.tril(chel_sun, -1))
#print np.sum(np.diag(chel_sun))
#print np.sum(np.triu(chel_sun, 1))