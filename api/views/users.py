from flask import Flask, Blueprint, request, jsonify, render_template
import requests
import json


user_blueprint = Blueprint('user_bp', __name__, template_folder='templates')


@user_blueprint.route('/')
def index():
    return render_template('users/index.html')