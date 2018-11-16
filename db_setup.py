import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key = True)
    userID = Column(String(20), nullable = False)
    userPWD = Column(String(40), nullable = False)
    
    @property
    def serialize(self):
        return {
            'id' : self.id,
            'userID' : self.userID,
            'userPWD' : self.userPWD
        }


engine = create_engine('sqlite:///UserInfo.db')
Base.metadata.create_all(engine)
