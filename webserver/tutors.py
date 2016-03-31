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

tutors_api = Blueprint('tutors_api', __name__)

@tutors_api.route('/gettutors',methods=['GET','POST'])
def getTutors():
  if not g.user.is_active:
    return redirect(url_for('login'))
  return render_template("tutors/tutors.html")

@tutors_api.route('/gettutorslist')
def getTutorsData():
  if not g.user.is_active:
    return redirect(url_for('login'))
  cursor = g.conn.execute("SELECT * FROM tutors")
  rowarray_list = []
  for result in cursor:
    t = {'enth_user':result['enth_user'],'artst_user':result['artst_user'],'salary':result['salary'],'status':result['status'],'rating':result['rating']}
    rowarray_list.append(t)
  json_string = json.dumps(rowarray_list)
  cursor.close()
  context = dict(data = json_string)
  return json_string

@tutors_api.route('/createtutors', methods=['GET','POST'])
def createTutors():
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    return render_template('tutors/createtutors.html')
  query = text("INSERT into tutors (enth_user, artst_user,salary,status,rating) VALUES (:enth_user, :artst_user,:salary,:status,:rating)")
  g.conn.execute(query, status=request.form['status'] ,rating=request.form['rating'],enth_user=request.form['enth_user'],artst_user=request.form['artst_user'],salary=request.form['salary'])
  return redirect('/tutors/gettutors')

@tutors_api.route('/updatetutors/<tutors_id>', methods=['GET','POST'])
def updateTutors(tutors_id):
  if not g.user.is_active:
    return redirect(url_for('login'))
  if request.method == 'GET':
    primary_key = tutors_id.split(",")
    enth_user = primary_key[0].strip()
    artst_user = primary_key[1].strip()
    query = text('SELECT * FROM tutors where enth_user=:enth_user and artst_user=:artst_user')
    result = g.conn.execute(query,enth_user=enth_user,artst_user=artst_user).fetchone()
    t = dict(enth_user=result['enth_user'],artst_user=result['artst_user'],salary=result['salary'],status=result['status'],rating=result['rating'])
    context = dict(data = t)
    return render_template('tutors/updatetutors.html',**context)
  primary_key = tutors_id.split(",")
  enth_user = primary_key[0].strip()
  artst_user = primary_key[1].strip()
  query = text("UPDATE tutors set status =:status, rating=:rating,salary=:salary where enth_user=:enth_user and artst_user=:artst_user")
  g.conn.execute(query, status=request.form['status'] ,rating=request.form['rating'],salary=request.form['salary'], enth_user=enth_user,artst_user=artst_user)
  return redirect('/tutors/gettutors')

@tutors_api.route('/deletetutors/<tutors_id>', methods=['GET','POST'])
def deleteTutors(tutors_id):
    if not g.user.is_active:
      return redirect(url_for('login'))
    primary_key = tutors_id.split(",")
    enth_user = primary_key[0].strip()
    artst_user = primary_key[1].strip()
    query = text('DELETE FROM tutors where enth_user=:enth_user and artst_user=:artst_user')
    g.conn.execute(query,enth_user=enth_user,artst_user=artst_user)
    return redirect('/tutors/gettutors')