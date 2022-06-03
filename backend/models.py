'''binds a flask application and a SQLAlchemy service'''
import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

DATABASE_NAME = "trivia"
DATABASE_PATH = "postgresql://{}/{}".format('localhost:5432', DATABASE_NAME)

db = SQLAlchemy()


def setup_db(app, database_path=DATABASE_PATH):
    '''db configurations'''
    app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_PATH
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Question(db.Model):
    '''defines quesrtions model'''
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        '''insert helper function'''
        db.session.add(self)
        db.session.commit()

    def update(self):
        '''update helper function'''
        db.session.commit()

    def delete(self):
        '''delete helper function'''
        db.session.delete(self)
        db.session.commit()

    def format(self):
        '''format helper function'''
        return {
          'id': self.id,
          'question': self.question,
          'answer': self.answer,
          'category': self.category,
          'difficulty': self.difficulty
        }


class Category(db.Model):
    '''defines category model'''
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        '''format helper function'''
        return {
          'id': self.id,
          'type': self.type
        }
