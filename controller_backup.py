import os
import sys
import httplib2
import json
import requests
import string

from flask import Flask, render_template, request, redirect
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

from db_setup import Base, User
from flask import make_response
#from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)

engine = create_engine('sqlite:///UserInfo.db')
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session=DBSession()

#db = SQLAlchemy(app)

@app.route('/')
@app.route('/main')
def showMain():
    #main private, public seperate
    return render_template('main.html')


@app.route('/signUp', methods = ['GET','POST'])
def showSignUp():
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


@app.route('/signIn', methods = ['GET', 'POST'])
def showSignIn():
    users = session.query(User).all()
    num = len(users)

    if request.method == 'POST':
        reqUserID = request.form['userID']
        reqUserPWD = request.form['userPWD']
#이건 그냥 db 체크고 진짜 세션도 바꿔야 함 - 이전 코드 더 참고하기
        for i in range(num):
            checkUserID = users[i].userID
            if(reqUserID == checkUserID):
                checkUserPWD = users[i].userPWD
                if(reqUserPWD == checkUserPWD):
                    flash("Hello %s :)" % reqUserID)
                    return redirect(url_for('showUserPage'))
                else:
                    flash("Wrong PWD")
                    return redirect(url_for('showMain'))
            else:
                flash("Wrong ID")
                return redirect(url_for('showMain'))
    return render_template('signIn.html')


@app.route('/user')
def showUserPage():
    return render_template('user.html')


@app.route('/users.json')
def showUsersJSON():
    users = session.query(User).all()
    return jsonify(Users=[u.serialize for u in users])


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
