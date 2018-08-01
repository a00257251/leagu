import flask
from flask_pymongo import PyMongo
from flask_mail import Mail, Message
from NBTextClassfier import classify1
from flask import Flask, make_response
import os
from json import dumps
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
##from upComingMatches import UPLR
from PostionClassfier import simulate_match,probalityA,probalityH
from newsapi import NewsApiClient
import requests
from flask_restful import reqparse, abort, Api, Resource
#from Result import main
#from PrimerLeagueTable import main
import json
import psycopg2
import urllib3
from time import sleep
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import subprocess
from flask_login import login_manager , login_user
from flask import Flask, Response, redirect, url_for, request, session, abort
from flask.ext.login import LoginManager, UserMixin, \
                                login_required, login_user, logout_user


from Tweeter import tweetSearch,selectTweets
import time
from datetime import datetime, date, time
#k =subprocess.check_output(['java', '-jar', 'tw.java'])
#line = k.stdout.read()
#print(k)
#p = subprocess.Popen(["java", "tw"], stdout=subprocess.PIPE)
#line = p.stdout.readline()
#print(line)

dt = datetime.now()
print dt
print dt.strftime("%A, %d. %B %Y %I:%M%p")


def UserInsertDash(username,team):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql2 = "INSERT INTO userdashtable (username, Team1) VALUES (%s, %s);"
    data = (str(username), str(team))
    print(data)
    cursor.execute(sql2, data)
    conn.commit()

def UserSelectDash(username):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select username, Team1 from userdashtable WHERE username= %s;", username)
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'username': item[0],
            'Team1': item[1]
            }
        comL.append(i)
    return comL

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

def player(team):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT  *  FROM player WHERE team = %s ", team)
    player = cursor.fetchall()
    return player



http = urllib3.PoolManager()

class GetOneItems(Resource):
    def get(self, _userId):
        try:
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

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    #"MAIL_USERNAME": os.environ['EMAIL_USER'],
    #"MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
    "MAIL_USERNAME": '',
    "MAIL_PASSWORD": ''
}

app.config.update(mail_settings)
mail = Mail(app)
mysql.init_app(app)
api = Api(app)
app.config["MONGO_URI"] = "mongodb://localhost:27017/Comm"
mongo = PyMongo(app)


api.add_resource(GetAllItems, '/rest/F')
api.add_resource(GetOneItems, '/rest/F/<_userId>')
nav = Navigation()
nav.init_app(app)
nav.Bar('top', [
    nav.Item('Home', 'index'),
    nav.Item('Table', 'view'),
    nav.Item('Match', 'Z'),
    nav.Item('Match Results', 'MatchesResult'),
    nav.Item('Fixtures', 'Fixtures'),
    nav.Item('Sign Up', 'showSignUp', items=[
        nav.Item('Log In', 'login')
    ]),
])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


class User(UserMixin):

    def __init__(self, id):
        self.id = id


    def __repr__(self):
        return "%d/%s/%s" % (self.id)

    @property
    def username(self):
        user = self.get_user()
        return user['username']

    @property
    def is_admin(self):
        user = self.get_user()
        return user['is_admin']

    def get_user(self):
        return find_user_by_id(self.id)


# some protected url
@app.route('/C')
@login_required
def home():
    return Response("Hello World!")

items_list = [];



# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        username = request.form['UserName']
        password = request.form['inputPassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_login', (username, password))
        data = cursor.fetchall()
        items_list = [];
        for item in data:
            i = {
                'id': item[0],
                'username': item[1],
                'password': item[2]
            }
            items_list.append(i)
        userjson = dumps(items_list)
        print(userjson)
        for i in items_list:
            id = i['id']
            uusername = i['username']

            print(id)
        if (items_list == []):
            return Response('<p>Wrong user</p>')
        Choses = UserSelectDash(uusername)
        if (Choses == []):
            resp1 = make_response((redirect('/loginChooses')))
            resp1.set_cookie('userID', uusername)
            user = User(id)
            login_user(user)
            return resp1
        else:
            resp = make_response((redirect('/loginDash')))
            resp.set_cookie('userID', uusername)
            user = User(id)
            login_user(user)
            return resp
    else:
        return render_template('loginn.html')



















userjson = dumps(items_list)
def find_user_by_id(user_id):
    for _user in items_list:
        if _user['id'] == user_id:
            return _user
    return None

def find_user_by_username(username):
    for _user in items_list:
        if _user['username'] == username:
            return _user
    return None


# somewhere to logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    resp = make_response((redirect('/')))
    resp.set_cookie('userID', "")
    return resp


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(userid):
    user = find_user_by_id(userid)
    return User(userid)


@app.route('/showSignUp')
def showSignUp():
    return render_template('signupp.html')

@app.route('/signUp', methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['fname']
        _lname = request.form['lname']
        _username = request.form['user']
        _tel = request.form['tel']
        _email = request.form['email']
        _password = request.form['pass']
        _timeDay = dt.strftime("%A, %d. %B %Y %I:%M%p")

        # validate the received values


            # All Good, let's call MySQL

        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc('sp_createUser', (_name, _lname, _tel, _username, _password, _email, _timeDay))
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
            resp = make_response((redirect('loginChooses')))
            resp.set_cookie('userID', _username)
            return resp
        else:
                return json.dumps({'error': str(data[0])})

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        return redirect('loginChooses')




@app.route('/' , methods=["GET","POST"])
def index():
    r = requests.get('https://newsapi.org/v2/top-headlines?sources=bbc-sport&apiKey=999a69895a874eb5859727b55b516dc6')
    jsonRequest = r.json()
   # articals = jsonRequest['articles']
    name = request.cookies.get('userID')
    dataH = [{'name': 'Team'}, {'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnley'},
             {'name': 'Manchester City'}, {'name': 'Manchester United'}, {'name': 'Liverpool'},
             {'name': 'Tottenham Hotspur'}, {'name': 'Leicester City'}, {'name': 'Everton'},
             {'name': 'Bournemouth'}, {'name': 'Watford'}, {'name': 'Brighton and Hove Albion'},
             {'name': 'Newcastle United'}, {'name': 'Swansea City'}, {'name': 'Huddersfield Town'},
             {'name': 'Crystal Palace'}, {'name': 'West Ham United'}, {'name': 'Southampton'},
             {'name': 'Stoke City'}, {'name': 'West Bromwich Albion'}
             ]

    search = TeamSearchForm(request.form)
    if request.method == 'POST':
        return search_results(search)
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT  DISTINCT Home,HS,Away,AAS FROM results LIMIT 8 ;''')
    MatchesResult = cursor.fetchall()
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT DISTINCT Home, Away , matchtime, matchdate FROM upcoming LIMIT 8''')
    Fixtures = cursor.fetchall()
    i = request.cookies.get('userID')
    if i == 'None':
        request.cookies.setdefault('Login')
    return render_template('Home.html',name=name,dataH=dataH, MatchesResult=MatchesResult,Fixtures=Fixtures)




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

@app.route('/view',methods=["GET"])
def view():
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT * FROM team ORDER by n ''')
    rv = cursor.fetchall()
    return render_template('index.html', rv=rv)





Match = []
@app.route('/rest/KK/<_userId>', methods=['GET','POST'])
def UU(_userId):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_GetOneItems', (_userId,))
    data = cursor.fetchall()


    for item in data:
        i = {
            'Id': item[0],
            'home': item[1],
            'away': item[2]
        }
        Match.append(i)
    print(Match)
    return dumps(Match)


def comsqlS(team):
    cursor = mysql.connect().cursor()
    cursor.execute("select  des, userid, chosenteam from com WHERE matchid = %s;", team)
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'des': item[0],
            'userid': item[1],
            'team': item[2]
        }
        comL.append(i)
    return comL

def comsqlSU(team):
    cursor = mysql.connect().cursor()
    cursor.execute("select  des, userid , chosenteam  from com WHERE userid = %s;", team)
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'des': item[0],
            'userid': item[1],
            'team': item[2]
        }
        comL.append(i)
    return comL


def comSql(idd,comment,name,chosenTeam):
    conn = mysql.connect()
    cursor = conn.cursor()
    _timeDay = dt.strftime("%A, %d. %B %Y %I:%M%p")
    sql2 = "INSERT INTO com (matchid, des, userid , chosenTeam ,timeDay) VALUES (%s, %s, %s, %s,%s);"
    data = (str(idd), str(comment), str(name), str(chosenTeam), str(_timeDay))
    print(data)
    cursor.execute(sql2, data)
    conn.commit()

@app.route('/Z', methods=['GET','POST'])
def Z():
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
                return render_template("MatchPrediction.html",H=H,A=A,D=D, g=g,  max=17000,
                                       set=zip(values, labels, colors),teamStat11=teamStat11,
                                           teamStat22=teamStat22,values=values, labels=labels,
                                            last1=last1, last2=last2,T1=T1,T2=T2
                                           , dataH=dataH, dataA=dataA)
    else:
           flash('Error: All the form fields are required.')
    return render_template("MatchPrediction.html",dataH=dataH, dataA=dataA)




@app.route('/M', methods=['GET','POST'])
@login_required
def M():

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

    if request.method == 'POST':
            for i in Match:
                iid = i['Id']
               # away = i['away']
                #home = i['home']
            #print(id)
            name = request.cookies.get('userID')
            print(name)
            #username = request.form.get['username']
            comment =  request.form['comment']
            print comment
            Team = request.form.get('Team_select')
            comSql(iid,comment,name,Team)
            comments = comsqlS(iid)
            print comments
            Team11 = request.form.get('Team11_select')
            Team22 = request.form.get('Team22_select')
            T1 = str(Team11)
            T2 = str(Team22)
            if T1 == T2:
              msg = 'The team cant play against itself!'
              return render_template("hij.html", msg=msg, dataH=dataH, dataA=dataA)
            else:
                print Team11, " ", Team22
                chel_sun = simulate_match(T1, T2, max_goals=4)
                last1= last3Home(T1)
                last2 = last3Away(T2)
                teamStat11 = sql(T1)
                teamStat22 = sql(T2)
                #HomeStat = probalityH(T1)
                #AwayStat = probalityH(T2)
                #HW =HomeStat[0]
                #HD = HomeStat[1]
                #HL = HomeStat[2]
                #AW = AwayStat[0]
                #AD = AwayStat[1]
                #AL = AwayStat[2]

                tt = T1+' VS '+T2
                print(tt)
               # tw = tweetSearch(tt)
                #stw = selectTweets(tt)
                H = np.sum(np.tril(chel_sun, -1))*100
                D = np.sum(np.diag(chel_sun))*100
                A = np.sum(np.triu(chel_sun, 1))*100

                colors = [
                    "#ff9933","#666699","#99003d"]
                values = [
                    A, D, H
                ]
                labels = [
                    T2, 'Drow', T1
                ]
                pie_labels = labels
                pie_values = values
                return render_template("Prediction.html",H=H,A=A,D=D, g=g,  max=17000,
                                       f=zip(values, labels, colors),teamStat11=teamStat11,
                                           teamStat22=teamStat22,values=values, labels=labels,
                                            last1=last1, last2=last2,T1=T1,T2=T2
                                           , dataH=dataH, dataA=dataA, comments=comments)#,HomeStat=HomeStat,AwayStat=AwayStat, AW=AW,HW=HW,AD=AD,HD=HD,AL=AL,HL=HL)
    else:
           flash('Error: All the form fields are required.')
    return render_template("hij.html",dataH=dataH, dataA=dataA)


@app.route('/loginDash', methods=['GET','POST'])
@login_required
def loginDash():
    name = request.cookies.get('userID')
    masseages = SelectMassage(name)
    comments = comsqlSU(name)
    userChooses = UserSelectDash(name)
    for Chooses in userChooses:
        Team11 = Chooses['Team1']
    T1 = str(Team11)
    print T1
    last1= last3Home(T1)
    last2 = last3Away(T1)
    teamStat11 = sql(T1)
    players = player(T1)
    #t = tweetSearch(T1)
    #tw = selectTweets(T1)
    Senders = SelectSenderMsg(name)
    SendersNames = SelectSenderNames(name)
    follow2 = mongo.db.friends.find({'name': name})
    print follow2
    Users = Allusers()
    return render_template("userIndex.html", g=g,  max=17000,
                          teamStat11=teamStat11,last1=last1,comments=comments,
                                last2=last2,T1=T1,players=players, name=name, masseages=masseages
                           , Senders=Senders, SendersNames=SendersNames, follow2=follow2, Users=Users)


@app.route('/loginChooses', methods=['GET','POST'])
@login_required
def loginChooses():

    dataH =  [{'name': 'Please Your favourite Team'},{'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnley'},
             {'name': 'Manchester City'}, {'name': 'Manchester United'}, {'name': 'Liverpool'},
             {'name': 'Tottenham Hotspur'}, {'name': 'Leicester City'}, {'name': 'Everton'},
             {'name': 'Bournemouth'}, {'name': 'Watford'}, {'name': 'Brighton and Hove Albion'},
             {'name': 'Newcastle United'}, {'name': 'Swansea City'}, {'name': 'Huddersfield Town'},
             {'name': 'Crystal Palace'}, {'name': 'West Ham United'}, {'name': 'Southampton'},
             {'name': 'Stoke City'}, {'name': 'West Bromwich Albion'}
             ]
    if request.method == 'POST':

            name = request.cookies.get('userID')
            masseages = SelectMassage(name)
            comments = comsqlSU(name)
            Team11 = request.form.get('Team11_select')
            T1 = str(Team11)
            print Team11
            UserInsertDash(name, T1)
            last1= last3Home(T1)
            last2 = last3Away(T1)
            teamStat11 = sql(T1)
            players = player(T1)
           # t = tweetSearch(T1)
           # tw = selectTweets(T1)
            Senders = SelectSenderMsg(name)
            SendersNames = SelectSenderNames(name)
            follow2 = mongo.db.friends.find({'name': name})
            print follow2
            Users = Allusers()
            return render_template("loginDash.html", g=g, max=17000,
                                   teamStat11=teamStat11, last1=last1, comments=comments,
                                   last2=last2, T1=T1, players=players, name=name, masseages=masseages
                                   , Senders=Senders, SendersNames=SendersNames, follow2=follow2, Users=Users)

    else:
           flash('Error: All the form fields are required.')
    return render_template("loginChooses.html",dataH=dataH)

@app.route('/team', methods=['GET','POST'])
def team():
    dataH =  [{'name': 'Please Choose Home Team'},{'name': 'Arsenal'}, {'name': 'Chelsea'}, {'name': 'Burnley'},
             {'name': 'Manchester City'}, {'name': 'Manchester United'}, {'name': 'Liverpool'},
             {'name': 'Tottenham Hotspur'}, {'name': 'Leicester City'}, {'name': 'Everton'},
             {'name': 'Bournemouth'}, {'name': 'Watford'}, {'name': 'Brighton and Hove Albion'},
             {'name': 'Newcastle United'}, {'name': 'Swansea City'}, {'name': 'Huddersfield Town'},
             {'name': 'Crystal Palace'}, {'name': 'West Ham United'}, {'name': 'Southampton'},
             {'name': 'Stoke City'}, {'name': 'West Bromwich Albion'}
             ]
    if request.method == 'POST':
            Team11 = request.form.get('Team11_select')
            T1 = str(Team11)
            tweets = tweetSearch(Team11)
            tw = selectTweets(Team11)
            print tw
            print Team11
            last1= last3Home(T1)
            last2 = last3Away(T1)
            teamStat11 = sql(T1)
            players = player(T1)
            return render_template("teampage.html", g=g,  max=17000,
                                  teamStat11=teamStat11,last1=last1,
                                   last2=last2,T1=T1,dataH=dataH,players=players,tw=tw)
    else:
           flash('Error: All the form fields are required.')
    return render_template("teampage.html",dataH=dataH)


@app.route('/MatchesResult', methods=['GET','POST'])
def MatchesResult():
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT Home,HS,Away,AAS, MatchDate FROM results ''')
    MatchesResult = cursor.fetchall()
    return render_template('MatchesResult.html', MatchesResult=MatchesResult)

@app.route('/rest/KK', methods=['GET','POST'])
def KK():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_GetAllItems')
    data = cursor.fetchall()
    items_list = [];
    for item in data:
        i = {
            'Id': item[0],
            'home': item[1],
            'time': item[2],
            'date': item[3],
            'away': item[4]
        }
        items_list.append(i)
    return dumps(items_list)



@app.route('/rest/TT', methods=['GET','POST'])
def TT():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_GetAllTeams')
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
          'N' :    cols[0],
          'Team' : cols[1],
          'Pl' :   cols[2],
          'W' : cols[3],
          'D' : cols[4],
          'L' : cols[5],
          'F' : cols[6],
          'A' : cols[7],
          'GD' : cols[8],
          'Pts' : cols[9]
        }
        items_list.append(i)
    return dumps(items_list)


@app.route('/rest/TT/<_userId>', methods=['GET', 'POST'])
def TTT(_userId):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('sp_GetOneTeams', (_userId,))
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
            'N': cols[0],
            'Team': cols[1],
            'Pl': cols[2],
            'W': cols[3],
            'D': cols[4],
            'L': cols[5],
            'F': cols[6],
            'A': cols[7],
            'GD': cols[8],
            'Pts': cols[9]
        }
        items_list.append(i)
    return dumps(items_list)

@app.route('/rest/UsersTT', methods=['GET', 'POST'])
def Usersss():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('GetAllusers')
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
            'id': cols[0],
            'userid': cols[1],
            'chosenteam': cols[2],
            'desc': cols[3]
        }
        items_list.append(i)
    return dumps(items_list)

@app.route('/rest/UsersTT/<_userId>', methods=['GET', 'POST'])
def Users(_userId):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.callproc('GetUser', (_userId,))
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
            'id': cols[0],
            'userid': cols[1]
        }
        items_list.append(i)
    return dumps(items_list)

@app.route('/Fixtures', methods=['GET','POST'])
def Fixtures():
    cursor = mysql.connect().cursor()
    cursor.execute('''SELECT * FROM upcoming ''')
    return render_template("upcoming.html")





#########################################################

def InsertMassage(sender,reciver,comment,timeDay,msgtype):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql2 = "INSERT INTO masseges (sender, reciver, comment, timeDay, msgtype) VALUES (%s, %s, %s, %s, %s);"
    data = (str(sender), str(reciver), str(comment), str(timeDay), str(msgtype))
    print(data)
    cursor.execute(sql2, data)
    conn.commit()

def DeleteMassage(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM masseges WHERE id = %s;" , id)
    conn.commit()

def DeleteUser(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM signup WHERE id = %s;" , id)
    conn.commit()

def uupdateUser(id,fname,lname,tel,email,username,upassword):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = ('''update signup set fname = %s, lname = %s, tel = %s, username = %s, upassword = %s, uemail = %s  WHERE id = %s;''')
    data =(fname,lname,tel,username,upassword,email,id)
    cursor.execute(sql,data)
    conn.commit()


def SelectMassage(reciver):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, sender, comment, reciver, timeday, msgtype from masseges WHERE reciver = %s ORDER BY id DESC;", str(reciver))
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'id' : item[0],
            'sender': item[1],
            'comment': item[2],
            'reciver' : item[3],
            'timeday': item[4],
            'msgtype': item[5]
        }
        comL.append(i)
    return comL


def Allusers():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, fname,lname,tel,username,upassword, uemail, timeday from signup ORDER BY id DESC;")
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'id' : item[0],
            'fname': item[1],
            'lname': item[2],
            'tel' : item[3],
            'username': item[4],
            'upassword': item[5],
            'uemail': item[6],
            'timeday': item[7]
        }
        comL.append(i)
    return comL


def userForgetPass(email):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select upassword from signup WHERE uemail = %s;", email)
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {

            'upassword': item[0]

        }
        comL.append(i)
    return comL



def SelectSenderNames(reciver):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT sender, timeDay from masseges WHERE reciver = %s ORDER BY id DESC;",reciver)
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'sender' : item[0],
            'timeDay': item[1]
        }
        comL.append(i)
    return comL

def SelectSenderCommentsALL(sender,reciver):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select comment,timeDay,id from masseges WHERE sender = %s and reciver = %s ORDER BY id DESC; ",(sender, reciver))
    comments = cursor.fetchall()
    cursor.execute("select comment,timeDay,id from masseges WHERE sender = %s and reciver = %s ORDER BY id DESC; ",
                   (reciver,sender))
    comments2 = cursor.fetchall()
    comL3 = []
    comL2 = []
    for item in comments:
        i = {
            'comment': item[0],
            'timeDay': item[1],
            'id': item[2]
        }
        comL2.append(i)
    comL3.append(comL2)
    comL = []
    for item in comments2:
        i = {
            'commentR' : item[0],
            'timeDayR': item[1],
            'idR':item[2]
        }
        comL.append(i)
    comL3.append(comL)
    return comL3


all = SelectSenderCommentsALL('osama','noor_algha')
print all

def SelectSenderComments(sender,reciver):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select comment,timeDay,id from masseges WHERE sender = %s and reciver = %s ORDER BY id DESC; ",(sender, reciver))
    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'comment' : item[0],
            'timeDay': item[1],
            'id':item[2]
        }
        comL.append(i)
    return comL


def SelectSenderCommentsR(reciver,sender):
    conn = mysql.connect()
    cursor = conn.cursor()
    sql = ('''select comment,timeDay,id from masseges WHERE sender = %s and reciver = %s ORDER BY id DESC ''')
    data = (str(reciver),str(sender))
    cursor.execute(sql, data)

    comments = cursor.fetchall()
    comL = []
    for item in comments:
        i = {
            'commentR' : item[0],
            'timeDayR': item[1],
            'idR':item[2]
        }
        comL.append(i)
    return comL


def SelectSenderMsg(sender):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, reciver, comment, timeDay from masseges WHERE sender = %s ORDER BY id DESC;", sender)
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
            'id': cols[0],
            'reciver': cols[1],
            'comment': cols[2],
            'timeDay':cols[3]
        }
        items_list.append(i)
    return items_list



@app.route('/')
def hello_world():
    name = request.cookies.get('userID')
    return render_template('Home2.html' , name=name)


@app.route('/UserMasseges', methods=['POST'])
@login_required
def UserMasseges():
    name = request.cookies.get('userID')
    sender = request.cookies.get('userID')
    print(sender)
    comment = request.form['M']
    print comment
    msgType = classify1(comment)
    reciver = request.form['name']
    timeDay = dt.strftime("%A, %d. %B %Y %I:%M%p")
    print(timeDay)
    InsertMassage(sender, reciver,comment,timeDay,msgType)
    folow = request.form['name']
    mongo.db.friends.insert([{"name": name,"follow": folow}])
    return redirect('/loginDash', code=201)


@app.route("/uploads", methods=["GET","POST"])
def save_upload():
    filename = photos.save(request.files['photo'])
    print(filename)
    return filename

@app.route("/uploads/<path:filename>")
def get_upload(filename):
    return mongo.send_file(filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST' and 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return filename
    return render_template('upload.html')

@app.route('/rest/Massages/<reciver>', methods=['GET'])
def SeeMag(reciver):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("select id, sender, comment,reciver ,timeDay from masseges WHERE reciver = %s ORDER BY id DESC;", reciver)
    data = cursor.fetchall()

    items_list = [];
    for cols in data:
        i = {
            'id': cols[0],
            'sender': cols[1],
            'comment': cols[2],
            'timeDay': cols[3]
        }
        items_list.append(i)
    return dumps(items_list)

@app.route('/rest/Massage/<sender>', methods=['GET'])
def SeeSendMag(sender):
    name = request.cookies.get('userID')
    sender = SelectSenderComments(sender,name)
    #recever = SelectSenderCommentsR(name,sender)
#    all = SelectSenderCommentsALL(sender,name)
    return dumps(sender)

@app.route('/rest/MassageR/<sender>', methods=['GET'])
def SeeReciveMag(sender):
    name = request.cookies.get('userID')
    #sender = SelectSenderComments(sender,name)
    recever = SelectSenderCommentsR(name,sender)
#    all = SelectSenderCommentsALL(sender,name)
    return dumps(recever)

@app.route('/rest/Massages/<_reciver>', methods=['DELETE'])
def DelMag(_reciver):
    DeleteMassage(int(_reciver))
    return "Hello"

@app.route('/rest/Users', methods=['GET'])
def getAllUsers():
    Users = Allusers()
    return dumps(Users)

@app.route('/rest/Userss/<_user>', methods=['DELETE'])
def DelUser(_user):
    DeleteUser(int(_user))
    return "Hello"

@app.route('/rest/Users/<_user>', methods=['POST'])
def UpdateUser(_user):
    fname = request.form['fname']
    lname = request.form['lname']
    username = request.form['username']
    tel = request.form['tel']
    uemail = request.form['uemail']
    upassword = request.form['upassword']
    uupdateUser(_user,fname,lname,tel,uemail,username,upassword)
    return redirect('/loginDash', code=200)

@app.route('/sforgot-password', methods=['GET'])
def sforgotPassword():
    return render_template('forgot-password.html')

@app.route('/forgotPassword', methods=['POST'])
def forgotPassword():
    _email = request.form['inputEmail']
    if app.app_context():
        password = userForgetPass(_email)
        for i in password:
            passw =  i['upassword']
        msg = Message(subject="Hello",
                      sender=app.config.get("MAIL_USERNAME"),
                      recipients=[_email],  # replace with your email for testing
                      body="your password is " + passw)
        mail.send(msg)
    return redirect('/',200)


if __name__ == '__main__':
    app.run()
