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

band_api = Blueprint('band_api', __name__)

@band_api.route('/getband',methods=['GET','POST'])
def getBand():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("band/band.html")

@band_api.route('/getbandlist')
def getBandData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM band")
  rowarray_list = []
  for result in cursor:
    t = {'band_id':result['band_id'],'band_name':result['band_name'],'since':str(result['since']),'specialization':result['specialization']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@band_api.route('/createband', methods=['GET','POST'])
def createBand():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('band/createband.html')
  since = datetime.strptime(request.form['since'], '%Y-%m-%d').date()
  query = text("INSERT into band (band_id, band_name,since,specialization) VALUES (:band_id,:band_name,:since,:specialization)")
  g.conn.execute(query, band_id=request.form['band_id'] ,band_name=request.form['band_name'],since=since,specialization=request.form['specialization'])
  return redirect('/band/getband')

@band_api.route('/updateband/<band_id>', methods=['GET','POST'])
def updateBand(band_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    query = text('SELECT * FROM band where band_id=:band_id')
    result = g.conn.execute(query,band_id=band_id).fetchone()
    t = dict(band_id=result['band_id'],band_name=result['band_name'],since=result['since'],specialization=result['specialization'])
    context = dict(data = t)
    return render_template('band/updateband.html',**context)
  since = datetime.strptime(request.form['since'], '%Y-%m-%d').date()
  query = text("UPDATE band set band_name =:band_name, since=:since, specialization=:specialization where band_id = :band_id")
  g.conn.execute(query, band_id=request.form['band_id'] ,band_name=request.form['band_name'],since=since,specialization=request.form['specialization'])
  return redirect('/band/getband')

@band_api.route('/deleteband/<band_id>', methods=['GET','POST'])
def deleteBand(band_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    query = text('DELETE FROM band where band_id=:band_id')
    g.conn.execute(query,band_id=band_id)
    return redirect('/band/getband')