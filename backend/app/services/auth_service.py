from flask import current_app
from flask_security import SQLAlchemyUserDatastore
from app.models import User, Role
from app.extensions import db

def init_user_datastore():
    from app.models import init_user_datastore
    return init_user_datastore(db)

def register_user(email, password, name):
    user_datastore = init_user_datastore()
    if user_datastore.get_user(email):
        return None, "Email already registered"
    
    user = user_datastore.create_user(
        email=email,
        password=password,
        name=name
    )
    db.session.commit()
    return user, None

def get_user_by_id(user_id):
    return User.query.get(user_id)