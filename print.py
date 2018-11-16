from flask import Flask
from flask import url_for, flash, jsonify
from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship

from db_setup import Base, User
#from flask import make_response
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

engine = create_engine('sqlite:///UserInfo.db')
Base.metadata.bind = create_engine

DBSession = sessionmaker(bind=engine)
session=DBSession()

db = SQLAlchemy(app)

users = session.query(User).all()

#print(type(users))

print("A lovely Bracket!")

s = session()
query = s.query(User).filter(User.userID.in_([reqUserID]), User.userPWD.in_([reqUserPWD]))
print(type(query))