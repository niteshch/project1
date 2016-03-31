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

bandmembers_api = Blueprint('bandmembers_api', __name__)

@bandmembers_api.route('/getbandmembers',methods=['GET','POST'])
def getBandmembers():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("bandmembers/bandmembers.html")

@bandmembers_api.route('/getbandmemberslist')
def getBandmembersData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM BAND_MEMBERS")
  rowarray_list = []
  for result in cursor:
    t = {'artst_user':result['artst_user'],'band_id':result['band_id'],'status':result['status']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@bandmembers_api.route('/createbandmembers', methods=['GET','POST'])
def createBandmembers():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('bandmembers/createbandmembers.html')
  query = text("INSERT into BAND_MEMBERS (artst_user,band_id,status) VALUES (:artst_user, :band_id,:status)")
  g.conn.execute(query, artst_user=request.form['artst_user'] ,band_id=request.form['band_id'],status=request.form['status'])
  return redirect('/bandmembers/getbandmembers')

@bandmembers_api.route('/updatebandmembers/<bandmembers_id>', methods=['GET','POST'])
def updateBandmembers(bandmembers_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    primary_key = bandmembers_id.split(",")
    artst_user = primary_key[0].strip()
    band_id = primary_key[1].strip()
    query = text('SELECT * FROM BAND_MEMBERS where artst_user=:artst_user and band_id=:band_id')
    result = g.conn.execute(query,artst_user=artst_user,band_id=band_id).fetchone()
    t = dict(artst_user=result['artst_user'],band_id=result['band_id'],status=result['status'])
    context = dict(data = t)
    return render_template('bandmembers/updatebandmembers.html',**context)
  primary_key = bandmembers_id.split(",")
  artst_user = primary_key[0].strip()
  band_id = primary_key[1].strip()
  query = text("UPDATE BAND_MEMBERS set status =:status where band_id=:band_id and artst_user=:artst_user")
  g.conn.execute(query, status=request.form['status'], band_id=band_id,artst_user=artst_user)
  return redirect('/bandmembers/getbandmembers')

@bandmembers_api.route('/deletebandmembers/<bandmembers_id>', methods=['GET','POST'])
def deleteBandmembers(bandmembers_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    primary_key = bandmembers_id.split(",")
    artst_user = primary_key[0].strip()
    band_id = primary_key[1].strip()
    query = text('DELETE FROM BAND_MEMBERS where band_id=:band_id and artst_user=:artst_user')
    g.conn.execute(query,band_id=band_id,artst_user=artst_user)
    return redirect('/bandmembers/getbandmembers')