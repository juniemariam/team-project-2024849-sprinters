from flask.cli import AppGroup
from .users import seed_users, undo_users, seed_restaurants, undo_restaurants, seed_reservations, undo_reservations, seed_reviews, undo_reviews,undo_menu_items

from backend.models.db import db, environment, SCHEMA

# Creates a seed group to hold our commands
# So we can type `flask seed --help`
seed_commands = AppGroup('seed')


# Creates the `flask seed all` command
@seed_commands.command('all')
def seed():
    users = seed_users()
    restaurants = seed_restaurants()
    seed_reservations(users, restaurants)
    seed_reviews(users, restaurants)
    # Add other seed functions here


# Creates the `flask seed undo` command
@seed_commands.command('undo')
def undo():
    undo_reviews()
    undo_reservations()
    undo_menu_items()
    undo_restaurants()
    undo_users()
    # Add other undo functions here