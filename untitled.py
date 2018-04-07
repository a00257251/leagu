from flask import Flask
import os
import numpy as np
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash, json
import mysql.connector
from mysql.connector import (connection)
from mysql.connector import errorcode
import pandas as pd
from flaskext.mysql import MySQL
from flask.ext.navigation import Navigation
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_login import login_required
#from nextMatch import get_last_matches
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField, SelectField
from results import PLR
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
#from upComingMatches import UPLR
from PostionClassfier import simulate_match
from newsapi import NewsApiClient
import requests
from flask_restful import reqparse, abort, Api, Resource
#from Result import main
from PrimerLeagueTable import main
import json
import psycopg2
import urllib3
from time import sleep
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

http = urllib3.PoolManager()

class GetOneItems(Resource):
    def get(self, _userId):
        try:
            # Parse the arguments
            # parser = reqparse.RequestParser()
            # parser.add_argument('id', type=str)
            # args = parser.parse_args()

            # _userId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetOneItems', (_userId,))
            data = cursor.fetchall()

            items_list = [];
            for item in data:
                i = {
                    'Id': item[0],
                    'home': item[1],
                    'away': item[2]
                }
                items_list.append(i)

            return {'StatusCode': '200', 'Items': items_list}

        except Exception as e:
            return {'error': str(e)}
class GetAllItems(Resource):
    def get(self):
        try:
            # Parse the arguments
            parser = reqparse.RequestParser()
            parser.add_argument('id', type=str)
            args = parser.parse_args()

            _userId = args['id']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_GetAllItems')
            data = cursor.fetchall()

            items_list=[];
            for item in data:
                i = {
                    'Id':item[0],
                    'home':item[1],
                    'away': item[2]
                }
                items_list.append(i)

            return {'StatusCode':'200','Items':items_list}

        except Exception as e:
            return {'error': str(e)}





def user_get():
    """
    This function retrieves a user's information.
    :param user_id: user ID
    :type user_id: int
    """
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_GetAllItems')
    data = cursor.fetchall()
    #prepare result
    items_list = [];
    for item in data:
        i = {
            'Id': item[0],
            'home': item[1],
            'away': item[2]
        }
        items_list.append(i)

        return {'StatusCode': '200', 'Items': items_list}







#url = ('https://newsapi.org/v2/top-headlines?'
#       'country=us&'
#       'apiKey=999a69895a874eb5859727b55b516dc6')
#response = requests.get(url)
#print response.json()


#newsapi = NewsApiClient(api_key='999a69895a874eb5859727b55b516dc6')


#top_headlines = newsapi.get_top_headlines(q='bitcoin',
#                                          sources='bbc-news,the-verge',
#                                          category='business',
#                                          language='en',
#                                          country='us')
#
#all_articles = newsapi.get_everything(q='bitcoin',
#                                      sources='bbc-news,the-verge',
#                                      domains='bbc.co.uk,techcrunch.com',
#                                      from_parameter='2017-12-01',
#                                      to='2017-12-12',
#                                      language='en',
#                                      sort_by='relevancy',
#                                      page=2)
#
#sources = newsapi.get_sources()
#print(sources)




class TeamSearchForm(Form):
    choices = [('Team', 'Team'),
               ('Team2', 'Team2')]
    select = SelectField('Search for Match:', choices=choices)
    search = StringField('')

mysql = MySQL()
DEBUG = True
app = Flask(__name__)
db = SQLAlchemy(app)

app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'admin'
app.config['MYSQL_DATABASE_DB'] = 'football'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)
api = Api(app)
api.add_resource(GetAllItems, '/F')
api.add_resource(GetOneItems, '/F/<_userId>')
nav = Navigation()
nav.init_app(app)
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Table', 'view'),
    nav.Item('Match', 'M'),
    nav.Item('Match Results', 'MatchesResult'),
    nav.Item('Fixtures', 'Fixtures'),
    nav.Item('Sign In', 'showSignUp', items=[
        nav.Item('Log In', 'login')
    ]),
])

@app.route('/user', methods=['GET'])
def form_user():
    result = user_get()
    return

#def requests_retry_session(
#    retries=3,
#    backoff_factor=0.3,
#    status_forcelist=(500, 502, 504),
#    session=None,
#):
#    session = session or requests.Session()
#    retry = Retry(
#        total=retries,
#        read=retries,
#        connect=retries,
#        backoff_factor=backoff_factor,
#        status_forcelist=status_forcelist,
#    )
#    adapter = HTTPAdapter(max_retries=retry)
#    session.mount('http://', adapter)
#    session.mount('https://', adapter)
#    return session
#
#response = requests_retry_session().get('http://127.0.0.1:5000')
#print(response.status_code)
#
#session = requests.Session()
#retry = Retry(connect=3, backoff_factor=0.5)
#adapter = HTTPAdapter(max_retries=retry)
#session.mount('http://', adapter)
#session.mount('https://', adapter)
#t = session.get("http://127.0.0.1:5000/F")
#print t
#import time
#r = ''
#s = requests.Session()
#k = s.mount('http://127.0.0.1:5000/F', HTTPAdapter(max_retries=5))

#s = requests.Session()
#
#retries = Retry(total=5,
#                backoff_factor=0.1,
#                status_forcelist=[ 500, 502, 503, 504 ])
#
#s.mount('http://', HTTPAdapter(max_retries=5))
#
#k = s.get('http://127.0.0.1:5000/F')
#print(k)
#while r == '':
#    try:
#        r = requests.get("http://127.0.0.1:5000/F")
#        jsonRequest = r.json()
#        k = jsonRequest["Items"]
#        print(k)
#    except requests.exceptions.ConnectionError:
#        print("Connection refused by the server..")
#        print("Let me sleep for 5 seconds")
#        print("ZZzzzz...")
#        time.sleep(5)
#        print("Was a nice sleep, now let me continue...")
#        continue
#

#r = requests.get('https://127.0.0.1:5000/F')
#jsonRequest = r.json()
#articals = jsonRequest['Items']
#print(articals)
#k = GetAllItems().get()
#print(k)


@app.route('/Liverpool', methods=['POST','GET'])
def hello():
    error = ""
    rows = None
    user_input = None
    data = None
    try:
        cursor = mysql.connect().cursor()
        if request.method == "POST":
            data = cursor.execute('''SELECT * FROM team WHERE Away = %s ''' , (request.form["search"],))
            data = cursor.fetchall()
            user_input = (request.form["search"],)
            return render_template("Home.html", data=data, user_input=user_input)

    except Exception as e:
        error = (str(e))
        print error
    return render_template("Home.html", error=error, user_input=user_input)



@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        cursor = mysql.connect().cursor()
        cursor.executemany('''SELECT * FROM liverpool WHERE name = %s ''', request.form['search'])
        return render_template("results.html", records=cursor.fetchall())
    return render_template('search.html')

@app.route('/' , methods=["GET","POST"])
def index():
    #newsapi = NewsApiClient(api_key='999a69895a874eb5859727b55b516dc6')

    #top_headlines = newsapi.get_top_headlines(q='bitcoin',
    #                                          sources='bbc-news,the-verge',
    #                                          category='business',
    #                                          language='en',
    #                                          country='us')
    #
    #all_articles = newsapi.get_everything(q='bitcoin',
    #                                      sources='bbc-news,the-verge',
    #                                      domains='bbc.co.uk,techcrunch.com',
    #                                      from_parameter='2017-12-01',
    #                                      to='2017-12-12',
    #                                      language='en',
    #                                      sort_by='relevancy',
    #                                      page=2)
    #
    #sources = newsapi.get_sources()
    ltitle       = []
    ldescription = []
    lurl         = []
    lurlToImage  = []
    lpublishedAt = []
    r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-sport&apiKey=999a69895a874eb5859727b55b516dc6')
    jsonRequest = r.json()
    articals = jsonRequest['articles']
    for art in articals:
        title           = art['title']
        ltitle      .append(title)
        description     = art["description"]
        ldescription.append(description)
        url             = art["url"]
        lurl        .append(url)
        urlToImage      = art["urlToImage"]
        lurlToImage .append(urlToImage)
        publishedAt     = art["publishedAt"]
        lpublishedAt.append(publishedAt)






    search = TeamSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT  DISTINCT Home,HS,Away,AAS FROM results ORDER by rid DESC LIMIT 8 ;''')
    MatchesResult = cursor.fetchall()
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT DISTINCT* FROM upcoming LIMIT 8''')
    Fixtures = cursor.fetchall()
    return render_template('Home.html', MatchesResult=MatchesResult,Fixtures=Fixtures , articals=articals ,
                           ltitle=ltitle ,ldescription=ldescription ,lurl=lurl ,lurlToImage=lurlToImage ,lpublishedAt=lpublishedAt )



@app.route('/results')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = '''SELECT * FROM team ORDER by n '''
        results = qry.all()

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        return render_template('results.html', results=results)


@app.route('/home')
def show_entries():
    cursor = mysql.connect().cursor()
    cursor.execute('SELECT * FROM Arsenal')
    table_rows = cursor.fetchall()
    #df = pd.DataFrame(table_rows)
    #df = pd.read_sql('SELECT * FROM Arsenal', cnx)
    return render_template('table_rows.html', table_rows=table_rows)


@app.route('/view',methods=["GET"])
def view():
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT * FROM team ORDER by n ''')
    rv = cursor.fetchall()
    return render_template('index.html', rv=rv)

@app.route('/reg/' , methods=["GET","POST"])
def reg():
    try:
        cursor = mysql.connect().cursor()
        return 'oket'
    except Exception as e:
        return (str(e)+'fghjk')


@app.route("/login")
def login():
    return render_template("login.html", title="data")


@app.route("/checkUser", methods=["POST"])
def check():
    username = str(request.form["user"])
    password = str(request.form["password"])
    cnx , cursor = connection()
    cursor.execute("SELECT name FROM user WHERE name ='" + username + "'")
    user = cursor.fetchone()
    if len(user) is 1:
        return redirect(url_for("home"))
    else:
        return "failed"

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.callproc('sp_createUser', (_name, _email, _password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message': 'User created successfully !'})
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return json.dumps({'html': '<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        return render_template('Home.html')



@app.route('/searc/', methods=['GET','POST'])
def Searc():
    error = ""
    rows = None
    user_input = None
    data = None
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM liverpool WHERE name = %s ", (request.form["search"],))
    data = cursor.fetchall()
    user_input = (request.form["search"])
    return render_template("Home.html", data=data, user_input=user_input)


class ReusableForm(Form):
    Team1 = TextField('Team1:', validators=[validators.required()])
    Team2 = TextField('Team2:', validators=[validators.required()])

class f(Form):
    Team11 = [{'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnly'}]

def sql(team):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * FROM team WHERE team = %s", team)
    teamStat = cursor.fetchall()
    return teamStat
def last3Home(team):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT DISTINCT home, hs , away, aas, MatchDate, result FROM results WHERE home = %s LIMIT 4 ", team)
    teamStat = cursor.fetchall()
    return teamStat
def last3Away(team):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT DISTINCT home, hs , away, aas, MatchDate, result  FROM results WHERE away = %s LIMIT 4 ", team)
    teamStat = cursor.fetchall()
    return teamStat
@app.route('/M', methods=['GET','POST'])
def M():
    #form = ReusableForm(request.form)
    dataH =  [{'name': 'Please Choose Home Team'},{'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnley'},
             {'name': 'Manchester City'}, {'name': 'Manchester United'}, {'name': 'Liverpool'},
             {'name': 'Tottenham Hotspur'}, {'name': 'Leicester City'}, {'name': 'Everton'},
             {'name': 'Bournemouth'}, {'name': 'Watford'}, {'name': 'Brighton and Hove Albion'},
             {'name': 'Newcastle United'}, {'name': 'Swansea City'}, {'name': 'Huddersfield Town'},
             {'name': 'Crystal Palace'}, {'name': 'West Ham United'}, {'name': 'Southampton'},
             {'name': 'Stoke City'}, {'name': 'West Bromwich Albion'}
             ]
    dataA = [{'name': 'Please Choose Away Team'}, {'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnley'},
            {'name': 'Manchester City'}, {'name': 'Manchester United'}, {'name': 'Liverpool'},
            {'name': 'Tottenham Hotspur'}, {'name': 'Leicester City'}, {'name': 'Everton'},
            {'name': 'Bournemouth'}, {'name': 'Watford'}, {'name': 'Brighton and Hove Albion'},
            {'name': 'Newcastle United'}, {'name': 'Swansea City'}, {'name': 'Huddersfield Town'},
            {'name': 'Crystal Palace'}, {'name': 'West Ham United'}, {'name': 'Southampton'},
            {'name': 'Stoke City'}, {'name': 'West Bromwich Albion'}
            ]

    #Team11 = request.form('Team11_select')
    #Team22 = request.form('Team22_select')

   # print form.errors
    if request.method == 'POST':
            #Team1 = request.form['Team1']
            #Team2 = request.form['Team2']
            Team11 = request.form.get('Team11_select')
            Team22 = request.form.get('Team22_select')
            T1 = str(Team11)
            T2 = str(Team22)
            if T1 == T2:
              msg = 'The team cant play against itself!'
              return render_template("Prediction.html", msg=msg, dataH=dataH, dataA=dataA)
            else:
                #print Team1, " ", Team2
                print Team11, " ", Team22
                chel_sun = simulate_match(T1, T2, max_goals=10)
                #teamStat1 = sql(Team1)
                #teamStat2 = sql(Team2)
                last1= last3Home(T1)
                last2 = last3Away(T2)
                teamStat11 = sql(T1)
                teamStat22 = sql(T2)
                H = np.sum(np.tril(chel_sun, -1))
                D = np.sum(np.diag(chel_sun))
                A = np.sum(np.triu(chel_sun, 1))
                colors = [
                    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
                    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
                    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]
                values = [
                    A, D, H
                ]
                labels = [
                    T2, 'Drow', T1
                ]
                pie_labels = labels
                pie_values = values
       #         if form.validate():
                    # Save the comment here.
                  #  g = get_last_matches(Team1, Team2, 'H')

                 #   flash('Thanks for registration ' + Team1 + Team2)
                return render_template("Prediction.html",H=H,A=A,D=D, g=g,  max=17000,
                                       set=zip(values, labels, colors),teamStat11=teamStat11,
                                           teamStat22=teamStat22,values=values, labels=labels,
                                            last1=last1, last2=last2,T1=T1,T2=T2
                                           , dataH=dataH, dataA=dataA)
    else:
           flash('Error: All the form fields are required.')
    return render_template("Prediction.html",dataH=dataH, dataA=dataA)



@app.route('/MatchesResult', methods=['GET','POST'])
def MatchesResult():

    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT * FROM results ''')
    MatchesResult = cursor.fetchall()
    return render_template('MatchesResult.html', MatchesResult=MatchesResult)

@app.route('/Fixtures', methods=['GET','POST'])
def Fixtures():
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT * FROM upcoming ''')
    Fixtures = cursor.fetchall()
    #r = requests.get("http://127.0.0.1:5000/F")
    #jsonRequest = r.json()
    #k = jsonRequest["Items"]
    #print(k)
    # k = api.add_resource(GetAllItems, '/F')
    #k = GetAllItems()
    return render_template('upcoming.html',Fixtures=Fixtures)


if __name__ == '__main__':
    app.run()
