from flask import Blueprint, jsonify, abort, request

tasks_api = Blueprint('tasks_api', __name__, url_prefix='/api/v1/')

@tasks_api.route('tasks/', methods=['GET'], strict_slashes=False)
def tasks():
    '''Retrieves all tasks'''
    from api.views.db import Tasks
    tasks = Tasks.query.all()
    if tasks:
        return jsonify([task.to_dict() for task in tasks])
    return jsonify({"Error": "No tasks yet, add a task"})
@tasks_api.route('tasks/<int:userid>', methods=['GET'], strict_slashes=False)
def tasks_per_user(userid):
    '''Retrieves tasks for a specific user'''
    from api.views.db import Tasks, Users
    user = Users.query.filter_by(userid=userid)
    if user:
        user_tasks = Tasks.query.filter_by(userid=userid).all()
        if user_tasks:
            # if len(user_tasks) == 1:
                # return jsonify(len().to_dict())
            return jsonify([task.to_dict() for task in user_tasks])
        return jsonify({"Error": f"No tasks for user {userid} found"}), 400
    return jsonify({"Error": "User does not exist"})

@tasks_api.route('tasks/new/<int:userid>', methods=['POST'], strict_slashes=False)
def new_user_task(userid):
    '''adds a new task for a user'''
    from api.views.db import Tasks, Users
    from app import db
    from sqlalchemy.exc import IntegrityError
    user = Users.query.filter_by(userid=userid)
    if user:
        data = request.get_json()
        if data is None:
            return jsonify({"Error": "Not a JSON"}), 400
        if "title" not in data:
            return jsonify({"Error": "Task title is required"})
        if "description" not in data:
            return jsonify({"Error", "Description is required"})
        try:
            new_task = Tasks(title=data.get("title"), description=data.get("description"), userid=userid)
            db.session.add(new_task)
            db.session.commit()
            return jsonify(new_task.to_dict()), 201
        
        except IntegrityError as e:
            return jsonify({"Error": str(e.orig)})
            # db.session.rollback()
            # if 'tasks_title_key' in str(e.orig):
            #     return jsonify({"Error": "Title already exists"}), 400
            # elif 'tasks_description_key' in str(e.orig):
            #     return jsonify({"Error": "Description already exists"}), 400
            # else:
            #     return jsonify({"Error": f"An error occured while add a new tasks for user -> {userid}"}), 500
    return jsonify({"Error": "User not found"})
