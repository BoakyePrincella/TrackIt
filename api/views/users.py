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
                return redirect(url_for('user_bp.dashboard'))
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
                        return redirect(url_for('user_bp.signup'))
                    
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
            return redirect(url_for('user_bp.dashboard'))
            # print("Session retrieved on GET request:", user)
            # return jsonify({"user": user})
    
    return render_template('users/auth/signup.html')

taskss = [
    {"status": "Not Started"},
    {"status": "In Progress"},
    {"status": "Finished"},
    {"status": "In Progress"},
    {"status": "Not Started"},
    {"status": "Finished"}
]


@user_blueprint.route('/dashboard')
def dashboard():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
         # Calculate counts for statuses
        status_counts = {"Not Started": 0, "In Progress": 0, "Finished": 0}
        for task in taskss:
            status_counts[task["status"]] += 1
        
        # Dummy activities and timers data
        activities_count = len(taskss)  # or whatever logic to get your activities
        timers_count = 5  # example number of timers set

        return render_template("users/dashboard.html", status_counts=status_counts, activities_count=activities_count, timers_count=timers_count)
        
        # return render_template('users/dashboard.html') 
    status_counts = {"Not Started": 0, "In Progress": 0, "Finished": 0}
    for task in taskss:
        status_counts[task["status"]] += 1
    
    # Dummy activities and timers data
    activities_count = len(taskss)  # or whatever logic to get your activities
    timers_count = 5  # example number of 
    return render_template('users/base.html', content_template='users/dashboard.html', status_counts=status_counts, activities_count=activities_count, timers_count=timers_count)

@user_blueprint.route('/add-task', methods=['POST'])
def add_task():
    from app import db
    from api.views.db import Tasks, TaskStatus
    userid = session.get('user', {}).get('user_id')
    data = request.get_json()
    task_title = data.get('title')
    task_description = data.get('description')
    tstatus = data.get('tstatus')
    if userid:
        if task_title and task_description and isinstance(tstatus, int) :
            try:
                new_task = Tasks(userid=userid, status=TaskStatus(tstatus), title=task_title, description=task_description)
                db.session.add(new_task)
                db.session.commit()
                return jsonify({"message": f"Task saved. {task_title}"})
            except OperationalError:
                    return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        # print(task_title, task_description, tstatus)
        return jsonify({"message": "Title, description and status needed"})
    return redirect(url_for("user_bp.signin"))

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
            # elif response.status_code == 400:
            #     data = "No activies yet!"
                return render_template('users/time_tracker.html', tracker_history=data)
            return render_template('users/time_tracker.html')
        else:
            if response.status_code == 200:
                data = response.json()
            # elif response.status_code == 400:
            #     data = "No activies yet!"
                return render_template('users/base.html', content_template='users/time_tracker.html', tracker_history=data)
            return render_template('users/base.html', content_template='users/time_tracker.html')
    return redirect(url_for("user_bp.signin"))


@user_blueprint.route('/start-activity', methods=['POST'])
def start_activity():
    form_data = request.form
    activity = form_data.get('activity_name')
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return jsonify({"message": f"Activity - {activity} started", "start_time": start_time, "activity": f"{activity}" })

@user_blueprint.route('/stop-activity', methods=['POST'])
def stop_activity():
    data = request.get_json()
    elapsed_time = data.get('elapsed_time')
    # Here, you would typically save the elapsed_time to the database.
    return jsonify({"message": f"Activity stopped. Total elapsed time: {elapsed_time} seconds",})

@user_blueprint.route('/save-activity', methods=['POST'])
def save_activity():
    from datetime import time
    from api.views.db import Activities
    from app import db
    data = request.get_json()
    # elapsed_time = data.get('elapsed_time')
    elapsed_seconds = data.get('elapsed_time', 0)  # Defaults to 0 if not provided

    # Convert seconds to hours, minutes, and seconds
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Create a time object
    elapsed_time = time(hour=hours % 24, minute=minutes, second=seconds)
    activity = data.get('activity')
    user = data.get('user')
    # print( (type(elapsed_time), type(Activities.duration)))
    # return "Yes"

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

@user_blueprint.route('/start-timer', methods=['POST'])
def start_timer():
    userid = session.get('user', {}).get('user_id')
    if userid:
        form_data = request.form
        duration_whole = form_data.get('duration')
        if duration_whole:
            duration_div = duration_whole.split('.')
            minutes = int(duration_div[0]) if duration_div[0] else 0
            seconds = int(duration_div[1]) if len(duration_div) > 1 and duration_div[1] else 0
        else:
            minutes = 0
            seconds = 0
        if minutes != 0 or seconds != 0:
            return jsonify({"message": f"Timer set for {minutes} mins : {seconds} secs", "min": minutes, "sec": seconds})
        return jsonify({"message": f"Cannot set timer for {minutes} mins : {seconds} secs"})
    return redirect(url_for("user_bp.signin"))

@user_blueprint.route('/save-timer', methods=['POST'])
def save_timer():
    from datetime import time
    from api.views.db import Timers
    from app import db
    data = request.get_json()
    set_time = data.get('set_time', 0)
    # elapsed_seconds = data.get('elapsed_time', 0)  # Defaults to 0 if not provided

    # Convert seconds to hours, minutes, and seconds
    hours, remainder = divmod(set_time, 3600)
    minutes, seconds = divmod(remainder, 60)

    # Create a time object
    set_time = time(hour=hours % 24, minute=minutes, second=seconds)
    user = data.get('user')

    if user:
        if set_time:
            try:
                timer = Timers(userid=user, duration=set_time)
                db.session.add(timer)
                db.session.commit()
                return jsonify({"message": f"Timer saved. {set_time} seconds "})
            except OperationalError:
                    return render_template("error.html", message="Unable to connect to the server, Please check your network connection and try again")
        return jsonify({"message": "Set time needed"})
    return redirect(url_for("user_bp.signin"))

@user_blueprint.route('/timers-history', methods=['GET'])
def timer_history():
    userid = session.get('user', {}).get('user_id')
    if userid:
        act_url = f"{os.getenv('API_URL')}/timers/{userid}"
        response = requests.get(act_url)
        if response.status_code == 200:
            data = response.json()
            return render_template('components/timer_history.html', timer_history=data)
        return redirect(url_for("user_bp.signin"))
        
        
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