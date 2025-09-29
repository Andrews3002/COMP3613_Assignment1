from .user import initialize_user
from App.database import db

def initialize():
    db.drop_all()
    db.create_all()
    initialize_user()
