from flask import Flask, Blueprint, request, jsonify, render_template
import requests
import json


user_blueprint = Blueprint('user_bp', __name__, template_folder='templates', static_folder="static", static_url_path="/api/views/static")


@user_blueprint.route('/')
def index():
    return render_template('users/base.html')

@user_blueprint.route('/home')
def home():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('users/home.html')  
    return render_template('users/base.html', content_template='users/home.html')

@user_blueprint.route('/tasks')
def tasks():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('users/tasks.html')
    return render_template('users/base.html')

@user_blueprint.route('/time-tracker')
def time_tracker():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('users/time_tracker.html')
    return render_template('users/base.html', content_template='users/time_tracker.html')


@user_blueprint.route('/logout')
def logout():
    return "Logout here"