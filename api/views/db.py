from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime, Time, Enum
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from app import db
from .helper import format_datetime
from enum import Enum as PyEnum


class Users(db.Model):
    """ The users table """
    __tablename__ = 'users'
    userid = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(200))
    email = Column(String(200), unique=True)
    password = Column(String(200))

    tasks = relationship("Tasks", back_populates="user")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return self.userid
    
    def to_dict(self):
        return {
            "userid": self.userid,
            "user_name": self.username,
            "email": self.email
        }
        
class TaskStatus(PyEnum):
    NOT_STARTED = 0
    IN_PROGRESS = 1
    FINISHED = 2

class Tasks(db.Model):
    '''the tasks table'''
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    title = Column(String(255))
    description = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    status = Column(Enum(TaskStatus), default=TaskStatus.NOT_STARTED)
    
    
    user = relationship("Users", back_populates="tasks")
    
    def to_dict(self):
        return {
            "id": self.task_id,
            'userid': self.userid,
            'title': self.title,
            'description': self.description,
            "date_created": format_datetime(self.date_created),
            "status": self.status.name
        }

class Activities(db.Model):
    '''the activities table'''
    __tablename__ = 'activities'
    act_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    act_name = Column(String(255))
    duration = Column(Time)
    date = Column(DateTime, default=datetime.now())
    
    def to_dict(self):
        return {
            'userid': self.userid,
            'actiivity': self.act_name,
            'duration': self.duration.strftime('%H:%M:%S'),
            'date': format_datetime(self.date)
        }
        
class Timers(db.Model):
    '''the timers table'''
    __tablename__ = 'timers'
    timer_id = Column(Integer, primary_key=True, autoincrement=True)
    userid = Column(Integer, ForeignKey('users.userid'))
    duration = Column(Time)
    date = Column(DateTime, default=datetime.now())
    
    def to_dict(self):
        return {
            'userid': self.userid,
            'duration': self.duration.strftime('%H:%M:%S'),
            'date': format_datetime(self.date)
        }