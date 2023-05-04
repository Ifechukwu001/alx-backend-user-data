#!/usr/bin/env python3
"""Session authentication views
"""
from api.v1.views import app_views
from flask import request, jsonify, make_response, abort
from models.user import User
from os import getenv


@app_views.route("/auth_session/login",
                 methods=["POST"], strict_slashes=False)
def session_login():
    """Authenticates a new session"""
    email = request.form.get("email")
    if not email:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get("password")
    if not password:
        return jsonify({"error": "password missing"}), 400
    users = User.search({"email": email})
    if not len(users):
        return jsonify({"error": "no user found for this email"}), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response = make_response(user.to_json())
            response.set_cookie(getenv("SESSION_NAME"), session_id)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route("/auth_session/logout",
                 methods=["DELETE"], strict_slashes=False)
def delete_session():
    """Deletes a session
    """
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)
    return jsonify({})
