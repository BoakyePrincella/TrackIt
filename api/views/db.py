from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey, Text, DateTime
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.orm import relationship
from app import db

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
            "user_id": self.userid,
            "user_name": self.username,
            "email": self.email
        }
        
class Tasks(db.Model):
    '''the tasks table'''
    __tablename__ = 'tasks'
    task_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.userid'))
    title = Column(String(255))
    description = Column(Text)
    date_created = Column(DateTime, default=datetime.now())
    
    user = relationship("Users", back_populates="tasks")
    
    def to_dict(self):
        return {
            'user': self.user_id,
            'title': self.title,
            'description': self.description
        }
