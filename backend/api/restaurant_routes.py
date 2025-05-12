from flask import Blueprint, render_template, url_for, redirect, request, jsonify, current_app
from flask_login import current_user, login_user, logout_user, login_required
from sqlalchemy.ext.declarative import declarative_base
from ..models import Restaurant, Reservation, Review, SavedRestaurant, db
from ..forms import ReservationForm, ReviewForm

from flask_mail import Message


Base=declarative_base()

restaurant_routes = Blueprint("restaurant_routes", __name__, url_prefix="/api/restaurants")


# **************************** Restaurant Routes ******************************* #

# View all restaurants
@restaurant_routes.route("/", methods=["GET"])
def all_restaurants():
    all_restaurants = Restaurant.query.filter_by(is_approved=True).all()
    if all_restaurants:
        response = []
        for restaurant in all_restaurants:
            restaurant_obj = restaurant.to_dict()
            response.append(restaurant_obj)
        return { "Restaurants": response }, 200
    return { "Error": "No restaurants found" } , 404


# View one restaurant
@restaurant_routes.route("/<int:restaurant_id>", methods=["GET"])
def one_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return restaurant.to_dict(), 200
    return { "Error": "No restaurant found" } , 404



# Create new reservation
@restaurant_routes.route("/<int:restaurant_id>/reservations", methods=["POST"])
@login_required
def create_reservation(restaurant_id):
    reservation_form = ReservationForm()
    reservation_form['csrf_token'].data = request.cookies['csrf_token']
    
    from .. import mail

    if reservation_form.validate_on_submit():
        reservation_data = reservation_form.data

        new_reservation_data = Reservation()
        reservation_form.populate_obj(new_reservation_data)

        restaurant = Restaurant.query.get(restaurant_id)

        if restaurant:
            new_reservation = Reservation(
                user_id=current_user.id, 
                restaurant_id=restaurant.id, 
                reservation_time=reservation_data["reservation_time"],
                party_size=reservation_data["party_size"]
            )

            db.session.add(new_reservation)
            db.session.commit()
            new_reservation_obj = new_reservation.to_dict()
            print('------')
            print(current_user)

            try:
                # Make sure current_user has an email attribute
                # And that your User model has an email field.
                # If User model doesn't have 'name' or 'username', adjust the greeting.
                user_greeting_name = getattr(current_user, 'username', getattr(current_user, 'first_name', 'Valued Customer'))

                subject = f"Your Reservation at {restaurant.name} is Confirmed!"
                
                # Format reservation_time for better readability
                formatted_time = new_reservation.reservation_time.strftime("%A, %B %d, %Y at %I:%M %p")

                # Create an HTML body for a nicer email (optional, can use msg.body for plain text)
                html_body = render_template("email/reservation_confirmation.html",
                                            user_name=user_greeting_name,
                                            restaurant_name=restaurant.name,
                                            reservation_time=formatted_time,
                                            party_size=new_reservation.party_size)
                
                # Plain text body as a fallback
                text_body = f"""
Dear {user_greeting_name},

Your reservation at {restaurant.name} has been confirmed.

Details:
Date and Time: {formatted_time}
Table Size: {new_reservation.party_size}

We look forward to seeing you!

Sincerely,
The {restaurant.name} Team (BookTable)
"""

                msg = Message(subject,
                              recipients=[current_user.email],
                              body=text_body, # Plain text version
                              html=html_body) # HTML version
                
                mail.send(msg)
                current_app.logger.info(f"Reservation confirmation email sent to {current_user.email}")

            except Exception as e:
                current_app.logger.error(f"Failed to send reservation email to {current_user.email}: {e}")
                # Don't fail the entire request if email sending fails, the reservation is already made.
                # You could add a message to the response if you want to inform the user.
                # For example, by adding a key to new_reservation_obj:
                # new_reservation_obj['email_status'] = 'Failed to send confirmation email.'
            # --- End Email Sending ---
            
            return new_reservation_obj, 201
        return { "Error": "Restaurant not found" }, 404
    return { "Error": "Validation Error" }, 401


# View all restaurant reviews - Need to return number of reviews for each user
@restaurant_routes.route("/<int:restaurant_id>/reviews", methods=["GET"])
def restaurant_reviews(restaurant_id):
    reviews = Review.query.filter(Review.restaurant_id == restaurant_id).all()

    if reviews:
        response = []
        for review in reviews:
            review_obj = review.to_dict()
            response.append(review_obj)
        return response, 200
    return { "Error": "No reviews found" }, 404


# Create new review for restaurant
@restaurant_routes.route("/<int:restaurant_id>/reviews", methods=["POST"])
@login_required
def new_review(restaurant_id):
    review_form = ReviewForm()
    review_form['csrf_token'].data = request.cookies['csrf_token']

    if review_form.validate_on_submit():
        review_data = review_form.data

        new_review_data = Review()
        review_form.populate_obj(new_review_data)

        new_review = Review(
            user_id=current_user.id, 
            restaurant_id=restaurant_id, 
            review = review_data["review"],
            rating = review_data["rating"]
        )

        db.session.add(new_review)
        db.session.commit()
        new_review_obj = new_review.to_dict()
        return new_review_obj, 201
    return { "Error": "Validation Error" }, 401