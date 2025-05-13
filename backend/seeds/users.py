from backend.models import db, User, Restaurant, Reservation, Review, environment, SCHEMA, MenuItem
import datetime
from sqlalchemy import text

# ... other imports


# *********************************** Users **************************************** #
def seed_users():
    demo = User(username='Demo', email='demo@aa.io', password='password', first_name="Demo", last_name="User")
    james = User(username='jameslee', email='james@gmail.com', password='password', first_name="James", last_name="Lee")
    kyle = User(username='kyleware', email='kmware@mac.com', password='password', first_name="Kyle", last_name="Ware")
    jessica = User(username='jessicalee', email='jessica@gmail.com', password='password', first_name='Jessica', last_name='Lee')
    john = User(username='johnlee', email='john@gmail.com', password='password', first_name='John', last_name='Lee')
    jane = User(username='janelee', email='jane@gmail.com', password='password', first_name='Jane', last_name='Lee')
    susan = User(username='susanware', email='susan@gmail.com', password='password', first_name='Susan', last_name='Ware')
    mike = User(username='mikeware', email='mike@gmail.com', password='password', first_name='Mike', last_name='Ware')
    brent = User(username='brentware', email='brent@gmail.com', password='password', first_name='Brent', last_name='Ware')

    db.session.add_all([demo, james, kyle, jessica, john, jane, susan, mike, brent])
    db.session.commit()

    return {
        "demo": demo, "james": james, "kyle": kyle, "jessica": jessica,
        "john": john, "jane": jane, "susan": susan, "mike": mike, "brent": brent
    }

def undo_users():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.users RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM users"))
    db.session.commit()


# *********************************** Restaurants ************************************** #
def seed_restaurants():
    names = [
        "katsuya", "spago", "lawrys", "little_door", "granville", "catch", "bacari", "mortons",
        "yardbird", "seventy_one_above", "stk", "merois", "gracias_madre", "cecconis", "craigs"
    ]
    objects = []

    for name in names:
        rest = Restaurant(
            name=name.capitalize(),
            neighborhood="Testhood",
            address="123 Main Street",
            cuisines="Fusion",
            cost="$$",  # Your model expects a string, not an integer
            operation_hours="Mon-Fri 10:00-22:00",
            phone="(123) 456-7890",
            description="Test description...",
            website=f"http://{name}.com",
            preview_img=f"https://example.com/{name}.jpg",
            is_approved=True
        )
        objects.append(rest)

    db.session.add_all(objects)
    db.session.commit()

    return dict(zip(names, objects))

def undo_restaurants():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.restaurants RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM restaurants"))
    db.session.commit()


# *********************************** Reservations *************************************** #
def seed_reservations(users, restaurants):
    reservations = [
        ("james", "katsuya"), ("james", "spago"), ("kyle", "lawrys"), ("kyle", "little_door"),
        ("jessica", "granville"), ("john", "catch"), ("jane", "bacari"), ("james", "mortons"),
        ("kyle", "yardbird"), ("jessica", "seventy_one_above"), ("demo", "stk"), ("demo", "merois"),
        ("demo", "gracias_madre"), ("demo", "cecconis"), ("demo", "craigs")
    ]
    dt = datetime.datetime(2025, 2, 10, 2, 30)
    rsvps = [
        Reservation(user_id=users[u].id, restaurant_id=restaurants[r].id, reservation_time=dt, party_size=2)
        for u, r in reservations
    ]
    db.session.add_all(rsvps)
    db.session.commit()

def undo_reservations():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reservations RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reservations"))
    db.session.commit()


# *************************************** Reviews ******************************************** #
def seed_reviews(users, restaurants):
    data = [
        ("james", "katsuya", "Amazing fresh food...", 5),
        ("kyle", "spago", "Elegant place.", 4),
        ("jessica", "lawrys", "Perfect prime rib.", 5),
        ("john", "granville", "Very good brunch.", 4),
        ("jane", "catch", "Fun rooftop.", 5),
        ("demo", "stk", "Nice vibe.", 4)
    ]
    reviews = [
        Review(user_id=users[u].id, restaurant_id=restaurants[r].id, review=text, rating=rating)
        for u, r, text, rating in data
    ]
    db.session.add_all(reviews)
    db.session.commit()

def undo_reviews():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.reviews RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM reviews"))
    db.session.commit()

def undo_menu_items():
    if environment == "production":
        db.session.execute(f"TRUNCATE table {SCHEMA}.menu_items RESTART IDENTITY CASCADE;")
    else:
        db.session.execute(text("DELETE FROM menu_items"))
    db.session.commit()