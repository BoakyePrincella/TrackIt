from flask import Flask
from flask_caching import Cache
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os, uuid
load_dotenv()

app = Flask(__name__)
cache = Cache(app, config={'CACHE_TYPE': 'SimpleCache'})
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.debug = True
app.secret_key = os.getenv('SECRET_KEY', uuid.uuid4() )
db = SQLAlchemy(app)

#import blueprints
from api.views.users import user_blueprint
from api.v1.tasks import tasks_api
from api.v1.users import users_api

app.register_blueprint(user_blueprint)
app.register_blueprint(tasks_api)
app.register_blueprint(users_api)


if __name__ == '__main__':
    from app import app
    from api.views.db import *
    with app.app_context():
        db.create_all()
    app.run(port=5000)

