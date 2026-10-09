from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
CORS(app)

# Configuration JWT
app.config["JWT_SECRET_KEY"] = "change-this-secret-key"

jwt = JWTManager(app)

# Utilisateurs temporaires
users = []


# =========================
# REGISTER
# =========================
@app.route("/api/auth/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username et password sont obligatoires"
        }), 400

    # Vérifier si l'utilisateur existe
    for user in users:
        if user["username"] == username:
            return jsonify({
                "error": "Utilisateur déjà existant"
            }), 409

    # Hash du mot de passe
    hashed_password = generate_password_hash(password)

    user = {
        "id": len(users) + 1,
        "username": username,
        "password": hashed_password
    }

    users.append(user)

    return jsonify({
        "message": "Utilisateur créé avec succès",
        "username": username
    }), 201


# =========================
# LOGIN
# =========================
@app.route("/api/auth/login", methods=["POST"])
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username et password sont obligatoires"
        }), 400

    # Rechercher l'utilisateur
    user = next(
        (user for user in users if user["username"] == username),
        None
    )

    if user is None:
        return jsonify({
            "error": "Identifiants incorrects"
        }), 401

    # Vérifier le mot de passe
    if not check_password_hash(user["password"], password):
        return jsonify({
            "error": "Identifiants incorrects"
        }), 401

    # Générer le JWT
    access_token = create_access_token(
        identity=str(user["id"])
    )

    return jsonify({
        "message": "Connexion réussie",
        "access_token": access_token
    }), 200


# =========================
# USER CONNECTED
# =========================
@app.route("/api/auth/me", methods=["GET"])
@jwt_required()
def me():

    user_id = get_jwt_identity()

    user = next(
        (user for user in users if str(user["id"]) == user_id),
        None
    )

    if user is None:
        return jsonify({
            "error": "Utilisateur introuvable"
        }), 404

    return jsonify({
        "id": user["id"],
        "username": user["username"]
    })


# =========================
# TEST
# =========================
@app.route("/api/hello", methods=["GET"])
def hello():

    return jsonify({
        "message": "API Fast-Hosting fonctionne !"
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)