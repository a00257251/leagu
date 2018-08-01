from urllib2 import urlopen as urlO
from bs4 import BeautifulSoup as bs
from bs4 import Tag
import mysql.connector
from mysql.connector import errorcode
import csv
import pandas as pd
from sqlalchemy import create_engine
import MySQLdb
import ast

my_url = "http://www.skysports.com/premier-league-table"

cb = urlO(my_url)
page = cb.read()
html_soup = bs(page, "html.parser")


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



#
# data = []
# table = html_soup.find('table', attrs={'class':'standing-table__table'})
# table_body = table.find('tbody')
# rows = table_body.find_all('tr')
# for row in rows:
#      cols = row.find_all('td')
#      cols = [ele.text.strip().encode("utf8") for ele in cols]
#      data.append([ele for ele in cols if ele])
#     # data = [str(ele) for ele in cols]
# with open('Primier League Table5.csv', 'a') as outcsv:
#      # configure writer to write standard csv file
#      writer = csv.writer(outcsv, delimiter=',', lineterminator='\n')
#      writer.writerow(['N','Team',  'Pl',   'W',   'D',   'L',   'F' ,  'A' , 'GD',  'Pts'])
#      #for col in data:
#      for col in data:
#          outcsv.write('{0};'.format(col).strip().replace('[','').replace(']','').replace(';',''))
#          outcsv.write('\n')
#          # Write item to outcsv
#         #writer.writerow([col])
#


def Delete(T):
    bool(T)
    if  T is True :
      cursor.execute("DROP TABLE IF EXISTS team14")
      sql1 = """CREATE TABLE team14 (
  `N` int(11) DEFAULT NULL,
  `Team` varchar(45) NOT NULL,
  `Pl` int(11) DEFAULT NULL,
  `W` int(11) DEFAULT NULL,
  `D` int(11) DEFAULT NULL,
  `L` int(11) DEFAULT NULL,
  `F` int(11) DEFAULT NULL,
  `A` int(11) DEFAULT NULL,
  `GD` int(11) DEFAULT NULL,
  `Pts` int(11) DEFAULT NULL,
  PRIMARY KEY (Team)
    )"""
    cursor.execute(sql1)



def TableSearch(tableClass,index):

    table = html_soup.findAll('table', attrs={'class': tableClass})[int(index)].find_all('tr')[1:]
    for row in table:
      cols = row.findChildren(recursive=False)
      cols = [ele.text.strip().encode("utf8") for ele in cols]
      if cols:
          N = str(cols[0])
          Team = str(cols[1])
          Pl = str(cols[2])
          W = str(cols[3])
          D = str(cols[4])
          L = str(cols[5])
          F = str(cols[6])
          A = str(cols[7])
          GD = int(cols[8])
          Pts = str(cols[9])
          sql(N, Team, Pl, W, D, L,F,A,GD,Pts)

def sql(N, Team, Pl, W, D, L,F,A,GD,Pts):
    cursor = cnx.cursor()
    sql = "INSERT INTO team (N, Team, Pl, W, D, L,F,A,GD,Pts) VALUES (%s, %s, %s, %s, %s, %s,%s,%s, %s, %s);"
    data = (str(N), str(Team),str(Pl), str(W),str(D), str(L),str(F),str(A),str(GD),str(Pts))
    print(data)
    cursor.execute(sql, data)
    print(str(N), str(Team),str(Pl), str(W),str(D), str(L),str(F),str(A),str(GD),str(Pts))
    cnx.commit()

def main():
    tableClass = 'standing-table__table'
    i = 0
    TableSearch(tableClass, i)


#df = pd.DataFrame(pd.read_csv('Primier League Table5.csv', sep=',',dtype=str ))
#print df


#engine = create_engine("mysql://admin:admin@localhost/football")
#df=pd.DataFrame(['A','B'],columns=['new_tablecol'])
#df.to_sql(name='PremierLeague',con=engine,if_exists='append')

#print (df.head())
#print (df.tail())
#print(df['Team'])
#print(df['W']).astype(int)
# df.dtypes
#df['W']= df['W'].astype(str).astype(int)
#df.assign(C=df.W.str.replace(' %s ' ,''))
#df['W'] = df.W.str.replase("'","'").astype(int)
#df.apply(pd.to_numeric, errors='ignore')
#df['W'] = pd.to_numeric(df['W'])
#print df.dtypes