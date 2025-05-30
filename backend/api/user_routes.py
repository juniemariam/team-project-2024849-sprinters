from flask import Blueprint, jsonify
from flask_login import login_required, current_user
from ..models import User, db

# from app.models import favorites

user_routes = Blueprint('users', __name__, url_prefix="/api/users")

# ***************************************** User Routes ************************************ #

@user_routes.route('/')
@login_required
def users():
    """
    Query for all users and returns them in a list of user dictionaries
    """
    users = User.query.all()
    return {'users': [user.to_dict() for user in users]}


@user_routes.route('/<int:id>')
@login_required
def user(id):
    """
    Query for a user by id and returns that user in a dictionary
    """
    user = User.query.get(id)
    return user.to_dict()


# Get all user reservations
