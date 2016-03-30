#!/usr/bin/env python2.7

"""
Columbia W4111 Intro to databases
Example webserver

To run locally

    python server.py

Go to http://localhost:8111 in your browser


A debugger such as "pdb" may be helpful for debugging.
Read about it online.
"""

import os
import psycopg2
import json
from flask.ext.login import LoginManager
from sqlalchemy import *
from datetime import datetime
from User import User
from sqlalchemy.pool import NullPool
from flask import Flask, request, render_template, g, redirect, Response
from flask import Flask,session, flash, url_for, abort
from flask.ext.login import login_user , logout_user , current_user , login_required, UserMixin
from artist import artist_api
from band import band_api
from enthusiast import enthusiast_api
from event import event_api


tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
app = Flask(__name__, template_folder=tmpl_dir)

app.config.from_pyfile('app.cfg')
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(artist_api, url_prefix='/artist')
app.register_blueprint(band_api, url_prefix='/band')
app.register_blueprint(enthusiast_api, url_prefix='/enthusiast')
app.register_blueprint(event_api, url_prefix='/event')

@login_manager.user_loader
def load_user(user_id):
  return queryUser(user_id)

#
# The following uses the sqlite3 database test.db -- you can use this for debugging purposes
# However for the project you will need to connect to your Part 2 database in order to use the
# data
#
# XXX: The URI should be in the format of: 
#
#     postgresql://nitesch:$Heela79@w4111db.eastus.cloudapp.azure.com/nc2663
#
# For example, if you had username ewu2493, password foobar, then the following line would be:
#
#     DATABASEURI = "postgresql://ewu2493:foobar@w4111db.eastus.cloudapp.azure.com/ewu2493"
#
#DATABASEURI = "sqlite:///test.db"
DATABASEURI = "postgresql://postgres:@localhost:5432/museconnect"


engine = create_engine(DATABASEURI)


#engine.execute("""DROP TABLE IF EXISTS test;""")
#engine.execute("""DROP TABLE IF EXISTS users;""")
engine.execute("""CREATE TABLE IF NOT EXISTS users (
  user_id serial primary key,
  username varchar(10) unique,
  password varchar(20),
  email varchar(20) unique,
  active boolean,
  registered_on timestamp
);""")
engine.execute("""CREATE TABLE IF NOT EXISTS test (
  id serial,
  name text
);""")
# engine.execute("""INSERT INTO test(name) VALUES ('grace hopper');""")
# engine.execute("""INSERT INTO test(name) VALUES ('ada lovelace');""")
# engine.execute("""INSERT INTO test(name) VALUES ('alan turing');""")




@app.before_request
def before_request():
  """
  This function is run at the beginning of every web request 
  (every time you enter an address in the web browser).
  We use it to setup a database connection that can be used throughout the request

  The variable g is globally accessible
  """
  try:
    g.conn = engine.connect()
    g.user = current_user
  except:
    print "uh oh, problem connecting to database"
    import traceback; traceback.print_exc()
    g.conn = None

@app.teardown_request
def teardown_request(exception):
  """
  At the end of the web request, this makes sure to close the database connection.
  If you don't the database could run out of memory!
  """
  try:
    g.conn.close()
  except Exception as e:
    pass

@app.route('/')
def index():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("index.html")


# Example of adding new data to the database
@app.route('/add', methods=['POST'])
@login_required
def add():
  name = request.form['name']
  g.conn.execute('INSERT INTO test VALUES (NULL, ?)', name)
  return redirect('/')


@app.route('/login',methods=['GET','POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')
  
  username = request.form['username']
  password = request.form['password']
  registered_user = query(username=username,password=password)
  if registered_user is None:
    flash('Username or Password is invalid' , 'error')
    return redirect(url_for('login'))
  login_user(registered_user)
  flash('Logged in successfully')
  print 'Logged in successfully'
  return redirect(request.args.get('next') or url_for('index'))

@app.route('/register' , methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    create(request.form['username'] , request.form['password'],request.form['email'])
    # add user to database
    flash('User successfully registered')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index')) 


def query(username,password):
    query = text("SELECT * FROM users WHERE username = :uid and password = :pwd")
    result = g.conn.execute(query,uid=username,pwd=password)
    row = result.fetchone()
    result.close()
    if row is None:
      return row
    user = User(row['user_id'],row['username'],row['password'],row['email'],row['active'],row['registered_on'])
    return user

def queryUser(user_id):
    query = text("SELECT * FROM users WHERE user_id = :uid")
    result = g.conn.execute(query,uid=user_id)
    row = result.fetchone()
    result.close()
    if row is None:
      return row
    user = User(row['username'],row['password'],row['email'],row['active'],row['registered_on'])
    return user

def create(username ,password , email, active=True,registered_on=datetime.utcnow()):
    query = text("INSERT INTO users (username, password, email, active, registered_on) values (:uname, :pwd, :email_id, :is_active, :register_time) ")
    g.conn.execute(query,uname=username,pwd=password,email_id=email, is_active=active,register_time=registered_on)


if __name__ == "__main__":
  import click

  @click.command()
  @click.option('--debug', is_flag=True)
  @click.option('--threaded', is_flag=True)
  @click.argument('HOST', default='0.0.0.0')
  @click.argument('PORT', default=8111, type=int)
  def run(debug, threaded, host, port):
    """
    This function handles command line parameters.
    Run the server using

        python server.py

    Show the help text using

        python server.py --help

    """

    HOST, PORT = host, port
    print "running on %s:%d" % (HOST, PORT)
    app.run(host=HOST, port=PORT, debug=true, threaded=threaded)


  run()
