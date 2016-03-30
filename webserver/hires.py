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

hires_api = Blueprint('hires_api', __name__)

@hires_api.route('/gethires',methods=['GET','POST'])
def getHires():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("hires/hires.html")

@hires_api.route('/gethireslist')
def getHiresData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM hires")
  rowarray_list = []
  for result in cursor:
    t = {'enth_user':result['enth_user'],'artst_user':result['artst_user'],'event_id':result['event_id'],'status':result['status'],'rating':result['rating']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@hires_api.route('/createhires', methods=['GET','POST'])
def createHires():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('hires/createhires.html')
  query = text("INSERT into hires (enth_user, artst_user,event_id,status,rating) VALUES (:enth_user, :artst_user,:event_id,:status,:rating)")
  g.conn.execute(query, status=request.form['status'] ,rating=request.form['rating'],enth_user=request.form['enth_user'],artst_user=request.form['artst_user'],event_id=request.form['event_id'])
  return redirect('/hires/gethires')

@hires_api.route('/updatehires/<hires_id>', methods=['GET','POST'])
def updateHires(hires_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    primary_key = hires_id.split(",")
    enth_user = primary_key[0].strip()
    artst_user = primary_key[1].strip()
    event_id = int(primary_key[2])
    query = text('SELECT * FROM hires where enth_user=:enth_user and artst_user=:artst_user and event_id=:event_id')
    result = g.conn.execute(query,enth_user=enth_user,artst_user=artst_user,event_id=event_id).fetchone()
    t = dict(enth_user=result['enth_user'],artst_user=result['artst_user'],event_id=result['event_id'],status=result['status'],rating=result['rating'])
    context = dict(data = t)
    return render_template('hires/updatehires.html',**context)
  primary_key = hires_id.split(",")
  enth_user = primary_key[0].strip()
  artst_user = primary_key[1].strip()
  event_id = int(primary_key[2])
  query = text("UPDATE hires set status =:status, rating=:rating where enth_user=:enth_user and artst_user=:artst_user and event_id=:event_id")
  g.conn.execute(query, status=request.form['status'] ,rating=request.form['rating'],enth_user=enth_user,artst_user=artst_user,event_id=event_id)
  return redirect('/hires/gethires')

@hires_api.route('/deletehires/<hires_id>', methods=['GET','POST'])
def deleteHires(hires_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    primary_key = hires_id.split(",")
    enth_user = primary_key[0].strip()
    artst_user = primary_key[1].strip()
    event_id = int(primary_key[2])
    query = text('DELETE FROM hires where enth_user=:enth_user and artst_user=:artst_user and event_id=:event_id')
    g.conn.execute(query,enth_user=enth_user,artst_user=artst_user,event_id=event_id)
    return redirect('/hires/gethires')