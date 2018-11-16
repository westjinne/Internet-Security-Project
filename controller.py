import os
import sys
import httplib2
import json
import requests
import string

from flask import Flask, render_template, request, redirect, abort, session
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

from db_setup import *
from flask import make_response
from functools import wraps
from past.builtins import xrange
import random

app = Flask(__name__)

engine = create_engine('sqlite:///UserInfo.db')
Base.metadata.bind = create_engine


@app.route('/')
@app.route('/main')
def showMain():
    if not session.get('logged_in'):
        return render_template('main.html')
    else:
        return redirect(url_for('showUserPage'))


@app.route('/signUp', methods = ['GET','POST'])
def showSignUp():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.method == 'POST':
        newUser = User(
            userID = request.form['userID'],
            userPWD = request.form['userPWD'])
        session.add(newUser)
        session.commit()
        flash("New User Account %s Successfully Created!" % newUser.userID)
        return redirect(url_for('showMain'))
    else:
        return render_template('signUp.html')

    
@app.route('/signIn', methods=['GET', 'POST'])
def showSignIn():
    if request.method == 'POST':
        reqUserID = str(request.form['userID'])
        reqUserPWD = str(request.form['userPWD'])
        Session = sessionmaker(bind=engine)
        s = Session()
        query = s.query(User).filter(User.userID.in_([reqUserID]), User.userPWD.in_([reqUserPWD]))
        result = query.first()
        if result:
            session['logged_in'] = True
            flash("Welcome %s" % reqUserID)
        else:
            flash('Wrong PWD!')
        return showMain()
    else:
        return render_template('signIn.html')
    
    
@app.route('/signOut')
def showSignOut():
    session['logged_in'] = False
    return redirect(url_for('showMain'))


@app.route('/user')
def showUserPage():
    if not session.get('logged_in'):
        flash("You have to Sign In First")
        return redirect(url_for('showMain'))
    else:
        return render_template('user.html')
    

@app.route('/users.json')
def showUsersJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    users = session.query(User).all()
    return jsonify(Users=[u.serialize for u in users])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
