from flask import Blueprint, request, jsonify
from flask_security.utils import hash_password, verify_password, login_user
from app.models import user_datastore, User
from app import db
from flask_security import login_required, current_user

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    name = data["name"]
    role_name = data.get("role", "viewer")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    user = user_datastore.create_user(
        email=email,
        password=hash_password(password),
        name=name,
        roles=[role_name]
    )
    db.session.commit()
    return jsonify({"msg": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data["email"]
    password = data["password"]
    user = User.query.filter_by(email=email).first()

    if user and verify_password(password, user.password):
        login_user(user)
        return jsonify({
            "msg": "Login successful",
            "user": user.to_dict()
        })
    return jsonify({"msg": "Invalid email or password"}), 401


@auth_bp.route("/me", methods=["GET"])
@login_required
def me():
    return jsonify(current_user.to_dict())
