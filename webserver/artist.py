from flask import Blueprint

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

artist_api = Blueprint('artist_api', __name__)

@artist_api.route('/getartist',methods=['GET','POST'])
def getArtist():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("artist/artist.html")

@artist_api.route('/getartistlist')
def getArtistData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM artist")
  rowarray_list = []
  for result in cursor:
    t = {'username':result['username'],'email':result['email'],'user_password':result['user_password'],'address':result['address'],'first_name':result['first_name'],'middle_name':result['middle_name'],'last_name':result['last_name'],'experience':result['experience'],'specialization':result['specialization']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@artist_api.route('/createartist', methods=['GET','POST'])
def createArtist():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('artist/createartist.html')
  query = text("INSERT into artist (username, email,user_password, address, first_name, middle_name, last_name, experience, specialization) VALUES (:username,:email,:password,:address,:fname,:mname,:lname,:experience,:specialization)")
  g.conn.execute(query, username=request.form['username'] ,email=request.form['email'],password='123456',address=request.form['address'],fname=request.form['fname'],mname=request.form['mname'],lname=request.form['lname'],experience=int(request.form['experience']),specialization=request.form['specialization'])
  return redirect('/artist/getartist')

@artist_api.route('/updateartist/<username>', methods=['GET','POST'])
def updateArtist(username):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    query = text('SELECT * FROM artist where username=:username')
    result = g.conn.execute(query,username=username).fetchone()
    t = dict(username=result['username'],email=result['email'],user_password=result['user_password'],address=result['address'],first_name=result['first_name'],middle_name=result['middle_name'],last_name=result['last_name'],experience=result['experience'],specialization=result['specialization'])
    context = dict(data = t)
    return render_template('artist/updateartist.html',**context)

  query = text("UPDATE artist set email =:email, address=:address, first_name=:fname, middle_name=:mname, last_name=:lname, experience=:experience, specialization=:specialization where username = :username")
  g.conn.execute(query, username=request.form['username'] ,email=request.form['email'],address=request.form['address'],fname=request.form['fname'],mname=request.form['mname'],lname=request.form['lname'],experience=int(request.form['experience']),specialization=request.form['specialization'])
  return redirect('/artist/getartist')

@artist_api.route('/deleteartist/<username>', methods=['GET','POST'])
def deleteArtist(username):
    if not g.user.is_active:
      return redirect(url_for('login'))
    query = text('DELETE FROM artist where username=:username')
    print username
    g.conn.execute(query,username=username)
    return redirect('/artist/getartist')