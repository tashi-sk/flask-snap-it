import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/home")
def home():
    articles = mongo.db.article.find()
    return render_template("index.html", articles=articles)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if user already exists in db
        existing_user = mongo.db.users.find_one({
            "username": request.form.get("username").lower()
        })

        if existing_user:
            flash("Username already exists")
            return redirect(url_for('register'))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # put new user in session cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successfull")
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if existing username exists in database
        existing_user = mongo.db.users.find_one({
            "username": request.form.get("username").lower()
        })

        if existing_user:
            # ensure that hash password matches user input
            if check_password_hash(
                    existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")).upper())
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:
            # username doesnt exist
            flash("Incorrect Username and/or Password")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
