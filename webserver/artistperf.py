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

artistperf_api = Blueprint('artistperf_api', __name__)

@artistperf_api.route('/getartistperf',methods=['GET','POST'])
def getArtistperf():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("artistperf/artistperf.html")

@artistperf_api.route('/getartistperflist')
def getArtistperfData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM ARTIST_PERFORMANCE")
  rowarray_list = []
  for result in cursor:
    t = {'artst_user':result['artst_user'],'event_id':result['event_id']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@artistperf_api.route('/createartistperf', methods=['GET','POST'])
def createArtistperf():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('artistperf/createartistperf.html')
  query = text("INSERT into ARTIST_PERFORMANCE (artst_user,event_id) VALUES (:artst_user, :event_id)")
  g.conn.execute(query, artst_user=request.form['artst_user'] ,event_id=request.form['event_id'])
  return redirect('/artistperf/getartistperf')

# @artistperf_api.route('/updateartistperf/<artistperf_id>', methods=['GET','POST'])
# def updateArtistperf(artistperf_id):
#   if not g.user.is_active:
#     return redirect(url_for('login'))
#   if request.method == 'GET':
#     primary_key = artistperf_id.split(",")
#     artst_user = primary_key[0].strip()
#     band_id = primary_key[1].strip()
#     query = text('SELECT * FROM ARTIST_PERFORMANCE where artst_user=:artst_user and band_id=:band_id')
#     result = g.conn.execute(query,artst_user=artst_user,band_id=band_id).fetchone()
#     t = dict(artst_user=result['artst_user'],band_id=result['band_id'],status=result['status'])
#     context = dict(data = t)
#     return render_template('artistperf/updateartistperf.html',**context)
#   primary_key = artistperf_id.split(",")
#   artst_user = primary_key[0].strip()
#   band_id = primary_key[1].strip()
#   query = text("UPDATE ARTIST_PERFORMANCE set status =:status where band_id=:band_id and artst_user=:artst_user")
#   g.conn.execute(query, status=request.form['status'], band_id=band_id,artst_user=artst_user)
#   return redirect('/artistperf/getartistperf')

@artistperf_api.route('/deleteartistperf/<artistperf_id>', methods=['GET','POST'])
def deleteArtistperf(artistperf_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    primary_key = artistperf_id.split(",")
    artst_user = primary_key[0].strip()
    event_id = primary_key[1].strip()
    query = text('DELETE FROM ARTIST_PERFORMANCE where event_id=:event_id and artst_user=:artst_user')
    g.conn.execute(query,event_id=event_id,artst_user=artst_user)
    return redirect('/artistperf/getartistperf')