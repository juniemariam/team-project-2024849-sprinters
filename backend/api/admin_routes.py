from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from backend.models.model import Restaurant, Reservation
from backend.models import db
from datetime import datetime, timedelta
from sqlalchemy import func
from functools import wraps

admin_routes = Blueprint("admin", __name__, url_prefix="/api/admin")


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            return jsonify({"error": "Forbidden"}), 403
        return f(*args, **kwargs)

    return decorated_function


# GET /api/admin/restaurants
@admin_routes.route("/restaurants", methods=["GET"])
@login_required
@admin_required
def get_all_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([r.to_dict() for r in restaurants])


# PATCH /api/admin/approve/<restaurant_id>
@admin_routes.route("/approve/<int:restaurant_id>", methods=["PATCH"])
@login_required
@admin_required
def approve_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    restaurant.is_approved = True
    db.session.commit()
    return jsonify(restaurant.to_dict())


# DELETE /api/admin/delete/<restaurant_id>
@admin_routes.route("/delete/<int:restaurant_id>", methods=["DELETE"])
@login_required
@admin_required
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get_or_404(restaurant_id)
    db.session.delete(restaurant)
    db.session.commit()
    return jsonify({"message": "Restaurant deleted"})


# GET /api/admin/analytics
@admin_routes.route("/analytics", methods=["GET"])
@login_required
@admin_required
def reservation_analytics():
    last_month = datetime.utcnow() - timedelta(days=30)

    # Daily reservation counts
    daily_stats = db.session.query(
        func.date(Reservation.created_at),
        func.count(Reservation.id)
    ).filter(
        Reservation.created_at >= last_month
    ).group_by(
        func.date(Reservation.created_at)
    ).all()

    # Total reservations
    total_reservations = db.session.query(func.count(Reservation.id)).filter(
        Reservation.created_at >= last_month
    ).scalar()

    # Average party size
    avg_party_size = db.session.query(func.avg(Reservation.party_size)).filter(
        Reservation.created_at >= last_month
    ).scalar()

    # Top restaurant
    top_restaurant = db.session.query(
        Reservation.restaurant_id,
        func.count(Reservation.id)
    ).filter(
        Reservation.created_at >= last_month
    ).group_by(
        Reservation.restaurant_id
    ).order_by(func.count(Reservation.id).desc()).first()

    top_restaurant_name = None
    if top_restaurant:
        restaurant = Restaurant.query.get(top_restaurant[0])
        top_restaurant_name = restaurant.name if restaurant else None

    return jsonify({
        "daily": [{"date": str(d), "count": c} for d, c in daily_stats],
        "total": total_reservations,
        "average_party_size": round(avg_party_size or 0, 2),
        "top_restaurant": top_restaurant_name
    })
