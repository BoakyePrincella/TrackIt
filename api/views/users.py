from flask import Flask, Blueprint, request, jsonify, render_template
import requests
import json


user_blueprint = Blueprint('user_bp', __name__, template_folder='templates', static_folder="static", static_url_path="/api/views/static")


@user_blueprint.route('/')
def index():
    return render_template('users/index.html')

@user_blueprint.route('/tasks')
def tasks():
    return "Tasks here"

@user_blueprint.route('/time-tracker')
def time_tracker():
    return "Time tracker here"