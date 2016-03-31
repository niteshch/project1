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

bandperf_api = Blueprint('bandperf_api', __name__)

@bandperf_api.route('/getbandperf',methods=['GET','POST'])
def getBandperf():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("bandperf/bandperf.html")

@bandperf_api.route('/getbandperflist')
def getBandperfData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM BAND_PERFORMANCE")
  rowarray_list = []
  for result in cursor:
    t = {'band_id':result['band_id'],'event_id':result['event_id']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@bandperf_api.route('/createbandperf', methods=['GET','POST'])
def createBandperf():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('bandperf/createbandperf.html')
  query = text("INSERT into BAND_PERFORMANCE (band_id,event_id) VALUES (:band_id, :event_id)")
  g.conn.execute(query, band_id=request.form['band_id'] ,event_id=request.form['event_id'])
  return redirect('/bandperf/getbandperf')

# @bandperf_api.route('/updatebandperf/<bandperf_id>', methods=['GET','POST'])
# def updateBandperf(bandperf_id):
#   if not g.user.is_active:
#     return redirect(url_for('login'))
#   if request.method == 'GET':
#     primary_key = bandperf_id.split(",")
#     artst_user = primary_key[0].strip()
#     band_id = primary_key[1].strip()
#     query = text('SELECT * FROM ARTIST_PERFORMANCE where artst_user=:artst_user and band_id=:band_id')
#     result = g.conn.execute(query,artst_user=artst_user,band_id=band_id).fetchone()
#     t = dict(artst_user=result['artst_user'],band_id=result['band_id'],status=result['status'])
#     context = dict(data = t)
#     return render_template('bandperf/updatebandperf.html',**context)
#   primary_key = bandperf_id.split(",")
#   artst_user = primary_key[0].strip()
#   band_id = primary_key[1].strip()
#   query = text("UPDATE ARTIST_PERFORMANCE set status =:status where band_id=:band_id and artst_user=:artst_user")
#   g.conn.execute(query, status=request.form['status'], band_id=band_id,artst_user=artst_user)
#   return redirect('/bandperf/getbandperf')

@bandperf_api.route('/deletebandperf/<bandperf_id>', methods=['GET','POST'])
def deleteBandperf(bandperf_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    primary_key = bandperf_id.split(",")
    band_id = primary_key[0].strip()
    event_id = primary_key[1].strip()
    query = text('DELETE FROM BAND_PERFORMANCE where event_id=:event_id and band_id=:band_id')
    g.conn.execute(query,event_id=event_id,band_id=band_id)
    return redirect('/bandperf/getbandperf')