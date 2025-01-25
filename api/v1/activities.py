from flask import Blueprint, jsonify, abort, request

activities_api = Blueprint('activities', __name__, url_prefix='/api/v1/')

@activities_api.route('activities/', methods=['GET'], strict_slashes=False)
def tasks():
    '''Retrieves all activities'''
    from api.views.db import Activities
    activities = Activities.query.all()
    if activities:
        return jsonify([activity.to_dict() for activity in activities])
    return jsonify({"Error": "No activity yet, add an activity"})


@activities_api.route('activities/<int:userid>', methods=['GET'], strict_slashes=False)
def tasks_per_user(userid):
    '''Retrieves actiivities for a specific user'''
    from api.views.db import Activities, Users
    user = Users.query.filter_by(userid=userid)
    if user:
        user_actiivites = Activities.query.filter_by(userid=userid).all()
        if user_actiivites:
            # if len(user_tasks) == 1:
                # return jsonify(len().to_dict())
            return jsonify([activity.to_dict() for activity in user_actiivites])
        return jsonify({"Error": f"No activities found"}), 400
    return jsonify({"Error": "User does not exist"})

@activities_api.route('timers/<int:userid>', methods=['GET'], strict_slashes=False)
def timers_per_user(userid):
    '''Retrieves timers  for a specific user'''
    from api.views.db import Timers, Users
    user = Users.query.filter_by(userid=userid)
    if user:
        user_timers = Timers.query.filter_by(userid=userid).all()
        if user_timers:
            # if len(user_tasks) == 1:
                # return jsonify(len().to_dict())
            return jsonify([timer.to_dict() for timer in user_timers])
        return jsonify({"Error": f"No timers found"}), 400
    return jsonify({"Error": "User does not exist"})