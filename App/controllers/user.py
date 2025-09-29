from App.models import User
from App.models import Staff
from App.database import db

def initialize_user():
    newuser = User()
    db.session.add(newuser)
    db.session.commit()    
    return newuser
