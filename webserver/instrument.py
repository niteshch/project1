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

instrument_api = Blueprint('instrument_api', __name__)

@instrument_api.route('/getinstrument',methods=['GET','POST'])
def getInstrument():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("instrument/instrument.html")

@instrument_api.route('/getinstrumentlist')
def getInstrumentData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM INSTR_TRADES")
  rowarray_list = []
  for result in cursor:
    t = {'instr_id':result['instr_id'],'condition':result['condition'],'instr_type':result['instr_type'],'buyer_name':result['buyer_name'],'seller_name':result['seller_name'],'cost':result['cost'],'status':result['status']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@instrument_api.route('/createinstrument', methods=['GET','POST'])
def createInstrument():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('instrument/createinstrument.html')
  query = text("INSERT into INSTR_TRADES (instr_id, condition,instr_type,buyer_name,seller_name,cost,status) VALUES (:instr_id, :condition,:instr_type,:buyer_name,:seller_name,:cost,:status)")
  g.conn.execute(query, instr_id=request.form['instr_id'] ,condition=request.form['condition'],instr_type=request.form['instr_type'],buyer_name=request.form['buyer_name'],seller_name=request.form['seller_name'],cost=request.form['cost'],status=request.form['status'])
  return redirect('/instrument/getinstrument')

@instrument_api.route('/updateinstrument/<int:instr_id>', methods=['GET','POST'])
def updateInstrument(instr_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    query = text('SELECT * FROM INSTR_TRADES where instr_id=:instr_id')
    result = g.conn.execute(query,instr_id=instr_id).fetchone()
    t = dict(instr_id=result['instr_id'],condition=result['condition'],instr_type=result['instr_type'],buyer_name=result['buyer_name'],seller_name=result['seller_name'],cost=result['cost'],status=result['status'])
    context = dict(data = t)
    return render_template('instrument/updateinstrument.html',**context)
  query = text("UPDATE INSTR_TRADES set condition =:condition, instr_type=:instr_type, buyer_name=:buyer_name, seller_name=:seller_name, cost=:cost, status=:status where instr_id = :instr_id")
  g.conn.execute(query, instr_id=request.form['instr_id'] ,condition=request.form['condition'],instr_type=request.form['instr_type'],buyer_name=request.form['buyer_name'],seller_name=request.form['seller_name'],cost=request.form['cost'],status=request.form['status'])
  return redirect('/instrument/getinstrument')

@instrument_api.route('/deleteinstrument/<int:instr_id>', methods=['GET','POST'])
def deleteInstrument(instr_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    query = text('DELETE FROM INSTR_TRADES where instr_id=:instr_id')
    g.conn.execute(query,instr_id=instr_id)
    return redirect('/instrument/getinstrument')