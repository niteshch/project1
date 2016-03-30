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

enthusiast_api = Blueprint('enthusiast_api', __name__)

@enthusiast_api.route('/getenthusiast',methods=['GET','POST'])
def getEnthusiast():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("enthusiast/enthusiast.html")

@enthusiast_api.route('/getenthusiastlist')
def getEnthusiastData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM enthusiast")
  rowarray_list = []
  for result in cursor:
    t = {'username':result['username'],'email':result['email'],'enth_password':result['enth_password'],'address':result['address'],'first_name':result['first_name'],'middle_name':result['middle_name'],'last_name':result['last_name'],'interests':result['interests']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@enthusiast_api.route('/createenthusiast', methods=['GET','POST'])
def createEnthusiast():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('enthusiast/createenthusiast.html')
  query = text("INSERT into enthusiast (username, email,enth_password, address, first_name, middle_name, last_name, interests) VALUES (:username,:email,:password,:address,:fname,:mname,:lname,:interests)")
  g.conn.execute(query, username=request.form['username'] ,email=request.form['email'],password='123456',address=request.form['address'],fname=request.form['fname'],mname=request.form['mname'],lname=request.form['lname'],interests=request.form['interests'])
  return redirect('/enthusiast/getenthusiast')

@enthusiast_api.route('/updateenthusiast/<username>', methods=['GET','POST'])
def updateEnthusiast(username):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    query = text('SELECT * FROM enthusiast where username=:username')
    result = g.conn.execute(query,username=username).fetchone()
    t = dict(username=result['username'],email=result['email'],enth_password=result['enth_password'],address=result['address'],first_name=result['first_name'],middle_name=result['middle_name'],last_name=result['last_name'],interests=result['interests'])
    context = dict(data = t)
    return render_template('enthusiast/updateenthusiast.html',**context)

  query = text("UPDATE enthusiast set email =:email, address=:address, first_name=:fname, middle_name=:mname, last_name=:lname, interests=:interests where username = :username")
  g.conn.execute(query, username=request.form['username'] ,email=request.form['email'],address=request.form['address'],fname=request.form['fname'],mname=request.form['mname'],lname=request.form['lname'],interests=request.form['interests'])
  return redirect('/enthusiast/getenthusiast')

@enthusiast_api.route('/deleteenthusiast/<username>', methods=['GET','POST'])
def deleteEnthusiast(username):
    if not g.user.is_active:
      return redirect(url_for('login'))
    query = text('DELETE FROM enthusiast where username=:username')
    print username
    g.conn.execute(query,username=username)
    return redirect('/enthusiast/getenthusiast')