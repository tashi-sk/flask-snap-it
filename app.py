import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_args
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
        return redirect(url_for('profile', username=session["user"]))
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
                return redirect(url_for('profile', username=session["user"]))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for('login'))

        else:
            # username doesnt exist
            flash("Incorrect Username and/or Password")
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    username = mongo.db.users.find_one(
            {"username": session["user"]})

    if session["user"]:
        return render_template(
            "profile.html", username=username)
    return redirect(url_for('login'))


@app.route("/logout")
def logout():
    # deleting user from session cookie
    session.pop("user")
    flash("You have been Logged out successfully")
    return redirect(url_for("login"))


@app.route("/community")
def community():
    articles = mongo.db.article.find().sort("date", -1)
    # https://gist.github.com/mozillazg/69fb40067ae6d80386e10e105e6803c9
    # https://stackoverflow.com/questions/27992413/how-do-i-calculate-the-offsets-for-pagination/27992616
    # pylint: disable=unbalanced-tuple-unpacking
    page, per_page, offset = get_page_args(
        page_parameter='page', per_page_parameter='per_page',
        offset_parameter='offset')
    per_page = 5
    offset = (page - 1) * per_page
    total = mongo.db.article.find().count()
    article_paginated = articles[offset: offset + per_page]
    pagination = Pagination(page=page, per_page=per_page,
                            total=total)
    return render_template(
        "community.html", articles=article_paginated, page=page,
                           per_page=per_page,
                           pagination=pagination)


@app.route("/upload", methods=["GET", "POST"])
def upload():
    return render_template("upload.html")


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=True)
