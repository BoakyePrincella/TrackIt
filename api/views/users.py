from flask import Flask, Blueprint, request, jsonify, render_template, session, redirect, url_for, flash
import requests
import json
import os
from sqlalchemy.exc import OperationalError
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


user_blueprint = Blueprint('user_bp', __name__, template_folder='templates', static_folder="static", static_url_path="/api/views/static")


@user_blueprint.route('/')
def index():
    # method = request.args.get('method')
    user_data = session.get('user')
    if user_data:
        return render_template('users/base.html')
    else:
        return redirect(url_for("user_bp.signin"))

@user_blueprint.route('/signin', methods=['POST', 'GET'])
def signin():
    from api.views.db import Users
    error = None
    if request.method == "POST":
        form_data = request.form
        username = form_data.get("username")
        password = form_data.get("password")

        if not username or not password:
            error = "Userna`me and password are required."
            return render_template("users/auth/signin.html", error=error)

        try:
            user = Users.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session.permanent = True
                session['user'] = {"user_id":user.userid, "username": username, "username": user.username}
                # return jsonify({"user": session['user']})
                flash("You were successfully logged in")
                return redirect(url_for('user_bp.home'))
            else:
                error = "Invalid username or password"
        except OperationalError:
            return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
    
    return render_template("users/auth/signin.html", error=error)

@user_blueprint.route('/signup', methods=['POST', 'GET'])
def signup():
    from api.views.db import Users
    from app import db
    error = None
    if request.method == 'POST':
        form_data = request.form
        email = form_data.get('email')
        password1 = form_data.get('password1')
        password2 = form_data.get('password2')
        username = form_data.get('username')

        if password1 == password2:
            if email and username:
                # Check if the email or username already exists
                try:
                    existing_user = Users.query.filter((Users.email == email) | (Users.username == username)).first()
                
                    if existing_user:
                        if existing_user.email == email:
                            error = "Email already exists, signin instead"
                        elif existing_user.username == username:
                            error = "Username already exists, try another"
                    else:
                        new_user = Users(username=username, email=email)
                        new_user.set_password(password2)
                        db.session.add(new_user)
                        db.session.commit()
                        session.permanent = True
                        session['user'] = {"user_id":new_user.userid, "email": email, "username": username}
                        print(session['user'])
                        return redirect(url_for('user_bp.signup_complete'))
                    
                    return render_template('users/auth/signup.html', error=error)
                except OperationalError:
                    return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
                
            error = "Email and password required."
            return render_template('users/auth/signup.html', error=error)
        error = "Passwords do not match"
        return render_template('users/auth/signup.html', error=error)
    
    elif request.method == "GET":
        user = session.get("user")

        if user is None:
            return render_template('users/auth/signup.html')
        
        else:
            return redirect(url_for('user_bp.home'))
            # print("Session retrieved on GET request:", user)
            # return jsonify({"user": user})
    
    return render_template('users/auth/signup.html')

@user_blueprint.route('/home')
def home():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('users/home.html')  
    return render_template('users/base.html', content_template='users/home.html')

@user_blueprint.route('/tasks')
def tasks():
    userid = session.get('user', {}).get('user_id')
    if userid:
        url = f"{os.getenv('API_URL')}/tasks/{userid}"
        response = requests.get(url)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if response.status_code == 200:
                data = response.json()
                return render_template('users/tasks.html', data=data)
            msg = 'No data yet'
            return render_template('users/tasks.html/', msg=msg)
        else:
            if response.status_code == 200:
                data = response.json()   
                return render_template('users/base.html', content_template='users/tasks.html', data=data)
            msg = 'No data yet'
            return render_template('users/base.html/', content_template='users/tasks.html', msg=msg)
    return redirect(url_for("user_bp.signin"))

        # return render_template('users/base.html')

@user_blueprint.route('/time-tracker')
def time_tracker():
    userid = session.get('user', {}).get('user_id')
    if userid:
        act_url = f"{os.getenv('API_URL')}/activities/{userid}"
        response = requests.get(act_url)
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if response.status_code == 200:
                data = response.json()
            return render_template('users/time_tracker.html', tracker_history=data)
        else:
            if response.status_code == 200:
                data = response.json()
            return render_template('users/base.html', content_template='users/time_tracker.html', tracker_history=data)
    return redirect(url_for("user_bp.signin"))


@user_blueprint.route('/start-task', methods=['POST'])
def start_task():
    form_data = request.form
    task = form_data.get('task_name')
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message": f"Activity - {task} started", "start_time": start_time, "activity": f"{task}" })

@user_blueprint.route('/stop-task', methods=['POST'])
def stop_task():
    data = request.get_json()
    elapsed_time = data.get('elapsed_time')
    # Here, you would typically save the elapsed_time to the database.
    return jsonify({"message": f"Activity stopped. Total elapsed time: {elapsed_time} seconds",})

@user_blueprint.route('/save-task', methods=['POST'])
def save_task():
    from api.views.db import Activities
    from app import db
    data = request.get_json()
    elapsed_time = data.get('elapsed_time')
    activity = data.get('activity')
    user = data.get('user')

    if user:
        if elapsed_time and activity:
            try:
                new_activity = Activities(userid=user, act_name=activity, duration=elapsed_time)
                db.session.add(new_activity)
                db.session.commit()
                return jsonify({"message": f"Activity saved. {activity} - Total elapsed time: {elapsed_time} seconds by user {user}"})
            except OperationalError:
                    return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        return jsonify({"Error": "Time and activity needed"})
    return redirect(url_for("user_bp.signin"))
    # Here, you would typically save the elapsed_time to the database.

# @user_blueprint.route('/activities')
# def activities():
#     userid = session.get('user', {}).get('user_id')
#     if userid:
#         url = f"{os.getenv('API_URL')}/activities/{userid}"
#         response = requests.get(url)
#         if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
#             if response.status_code == 200:
#                 data = response.json()
#                 return render_template('users/time_tracker.html', tracker_history=data)
#             msg = 'No data yet'
#             return render_template('users/time_tracker.html/', tracker_msg=msg)
#         else:
#             if response.status_code == 200:
#                 data = response.json()   
#                 return render_template('users/base.html', content_template='users/time_tracker.html', tracker_history=data)
#             msg = 'No data yet'
#             return render_template('users/base.html/', content_template='users/time_tracker.html', tracker_msg=msg)
#     return redirect(url_for("user_bp.signin"))


@user_blueprint.route('/logout')
def logout():
    session.pop("user", None)
    return redirect(url_for("user_bp.signin"))