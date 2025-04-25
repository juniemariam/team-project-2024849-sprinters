from flask import Blueprint, render_template, url_for, redirect, request, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.ext.declarative import declarative_base
from ..models import Restaurant, Reservation, Review, SavedRestaurant, db
from ..forms import ReservationForm, ReviewForm


Base=declarative_base()

restaurant_routes = Blueprint("restaurant_routes", __name__, url_prefix="/api/restaurants")


# **************************** Restaurant Routes ******************************* #

# View all restaurants
@restaurant_routes.route("/", methods=["GET"])
def all_restaurants():
    all_restaurants = Restaurant.query.all()
    if all_restaurants:
        response = []
        for restaurant in all_restaurants:
            restaurant_obj = restaurant.to_dict()
            response.append(restaurant_obj)
        return { "Restaurants": response }, 200
    return { "Error": "No restaurants found" } , 404


# View one restaurant
