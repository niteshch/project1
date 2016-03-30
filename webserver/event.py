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

event_api = Blueprint('event_api', __name__)

@event_api.route('/getevent',methods=['GET','POST'])
def getEvent():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("event/event.html")

@event_api.route('/geteventlist')
def getEventData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM event")
  rowarray_list = []
  for result in cursor:
    t = {'event_id':result['event_id'],'start_time':str(result['start_time']),'end_time':str(result['end_time']),'address':result['address'],'event_type':result['event_type']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@event_api.route('/createevent', methods=['GET','POST'])
def createEvent():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('event/createevent.html')
  start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
  end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M:%S')
  query = text("INSERT into event (event_id, start_time,end_time,address,event_type) VALUES (:event_id,:start_time,:end_time,:address,:event_type)")
  g.conn.execute(query, event_id=request.form['event_id'] ,start_time=start_time,end_time=end_time,address=request.form['address'],event_type=request.form['event_type'])
  return redirect('/event/getevent')

@event_api.route('/updateevent/<int:event_id>', methods=['GET','POST'])
def updateEvent(event_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    query = text('SELECT * FROM event where event_id=:event_id')
    result = g.conn.execute(query,event_id=event_id).fetchone()
    print result
    t = dict(event_id=result['event_id'],start_time=result['start_time'],end_time=result['end_time'],address=result['address'],event_type=result['event_type'])
    context = dict(data = t)
    print context
    return render_template('event/updateevent.html',**context)
  start_time = datetime.strptime(request.form['start_time'], '%Y-%m-%d %H:%M:%S')
  end_time = datetime.strptime(request.form['end_time'], '%Y-%m-%d %H:%M:%S')
  query = text("UPDATE event set start_time =:start_time, end_time=:end_time, address=:address, event_type=:event_type where event_id = :event_id")
  g.conn.execute(query, event_id=request.form['event_id'] ,start_time=request.form['start_time'],end_time=end_time,address=request.form['address'],event_type=request.form['event_type'])
  return redirect('/event/getevent')

@event_api.route('/deleteevent/<int:event_id>', methods=['GET','POST'])
def deleteEvent(event_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    query = text('DELETE FROM event where event_id=:event_id')
    g.conn.execute(query,event_id=event_id)
    return redirect('/event/getevent')