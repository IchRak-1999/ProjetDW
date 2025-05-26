from flask import Blueprint, jsonify, request
from models import User, session

api = Blueprint("api", __name__)

@api.route("/users", methods=["GET"])
def get_users():
    users = session.query(User).all()
    return jsonify([{"id": u.id, "name": u.name} for u in users])

@api.route("/users", methods=["POST"])
def add_user():
    data = request.json
    new_user = User(name=data["name"])
    session.add(new_user)
    session.commit()
    return jsonify({"message": "User added"}), 201
