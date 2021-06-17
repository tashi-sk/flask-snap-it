import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from flask_paginate import Pagination, get_page_args
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
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
    articles = mongo.db.article.find().sort("date", -1)
    # get the session user #'s username from cookie
    username = mongo.db.users.find_one(
            {"username": session["user"]})

    if session["user"]:
        return render_template(
            "profile.html", username=username, articles=list(articles))
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
    if request.method == "POST":
        # to get current date and time
        now_date = datetime.now().strftime('%d,%b')
        now_time = datetime.now()
        current_time = str(now_time.hour)+":"+str(now_time.minute)
        # converting time to am/pm 
        if now_time.hour > 12:
            current_time = str(now_time.strftime('%H:%M'))+"pm"
        else:
            current_time = str(now_time.strftime('%H:%M'))+"am"
        username = mongo.db.users.find_one(
            {"username": session["user"]})
        # Inserting Post to db
        if username:
            new_post = {
                "image": request.form.get("image_url"),
                "title": request.form.get("title"),
                "summary": request.form.get("summary"),
                "submit_by": session["user"].lower(),
                "date": now_date,
                "time": current_time
            }
            mongo.db.article.insert_one(new_post)
            flash("Post submitted successfully")
            return redirect(url_for('profile', username=username))
    return render_template("upload.html")


@app.route("/edit_post/<post_id>", methods=["GET", "POST"])
def edit_post(post_id):
    if request.method == "POST":
        # to get current date and time
        now_date = datetime.now().strftime('%d,%b')
        now_time = datetime.now()
        current_time = str(now_time.hour)+":"+str(now_time.minute)
        # converting time to am/pm 
        if now_time.hour > 12:
            current_time = str(now_time.strftime('%H:%M'))+"pm"
        else:
            current_time = str(now_time.strftime('%H:%M'))+"am"

        username = mongo.db.users.find_one(
            {"username": session["user"]})
        # Edit choosen user post 
        new_post = {
            "image": request.form.get("image_url"),
            "title": request.form.get("title"),
            "summary": request.form.get("summary"),
            "submit_by": session["user"].lower(),
            "date": now_date,
            "time": current_time
        }
        # update choosen user post 
        mongo.db.article.update({"_id": ObjectId(post_id)}, new_post)
        flash("Post Updated successfully")
        return redirect(url_for('profile', username=username))

    post = mongo.db.article.find_one({"_id": ObjectId(post_id)})
    articles = mongo.db.article.find().sort("title", 1)
    return render_template("edit_post.html", post=post, articles=articles)


@app.route("/delete_post/<post_id>")
def delete_post(post_id):
    # removing article post of user 
    mongo.db.article.remove({"_id": ObjectId(post_id)})
    flash("Post Successfully deleted")
    return redirect(url_for("profile", username=session["user"]))


@app.route("/comments/<post_id>", methods=["GET", "POST"])
def comments(post_id):
    post = mongo.db.article.find_one({"_id": ObjectId(post_id)})
    articles = mongo.db.article.find()
    comments = mongo.db.comments.find().sort("date", -1)
    if request.method == "POST":
        # current date and time
        now_date = datetime.now().strftime('%d-%b')
        now_time = datetime.now()
        current_time = str(now_time.hour)+":"+str(now_time.minute)
        if now_time.hour > 12:
            current_time = str(now_time.strftime('%H:%M'))+"pm"
        else:
            current_time = str(now_time.strftime('%H:%M'))+"am"
        # insert new comment in db
        new_comment = {
                "comment_id": ObjectId(post_id),
                "comment": request.form.get("userComment"),
                "submit_by": session["user"].lower(),
                "date": now_date,
                "time": current_time,
            }

        mongo.db.comments.insert_one(new_comment)
        flash("Comment Added")
        return render_template(
            'comments.html', articles=articles, post=post, comments=comments)

    return render_template(
        'comments.html', articles=articles, post=post, comments=comments)


@app.route("/edit_comment/<comment_id>", methods=["GET", "POST"])
def edit_comment(comment_id):

    articles = mongo.db.article.find()
    post_comments = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    comments = mongo.db.comments.find().sort("date", -1)

    for k, v in post_comments.items():
        if k == "comment_id":
            post_id = v

    post = mongo.db.article.find_one({"_id": ObjectId(post_id)})
         
    if request.method == "POST":
        # current date and time
        now_date = datetime.now().strftime('%d-%b')
        now_time = datetime.now()
        current_time = str(now_time.hour)+":"+str(now_time.minute)
        if now_time.hour > 12:
            current_time = str(now_time.strftime('%H:%M'))+"pm"
        else:
            current_time = str(now_time.strftime('%H:%M'))+"am"
        edited_comment = {
            "comment": request.form.get("userEditComment"),
            "edit": " (edited)",
            "date": now_date,
            "time": current_time
        }
        mongo.db.comments.update_one(
            {"_id": ObjectId(comment_id)}, {"$set": edited_comment})
        flash("Comment Updated successfully")
        return render_template(
            'comments.html', post=post, comments=comments, articles = articles)

    return render_template(
        "edit_comment.html", post=post, post_comments=post_comments)


@app.route("/delete_comment/<comment_id>")
def delete_comment(comment_id):
    # find comments in db with comment_id
    post_comments = mongo.db.comments.find_one({"_id": ObjectId(comment_id)})
    # get all articles post from db
    articles = mongo.db.article.find()
    # getting comment_id from comments db to give as post_id on comments.html
    for k,v in post_comments.items():
        if k == "comment_id":
            post_id = v

    # get the article post from db where user was deleteing comment
    post = mongo.db.article.find_one({"_id": ObjectId(post_id)})
    # sorting comments for post by date
    comments = mongo.db.comments.find().sort("date", -1)
    # removing user selected comment
    mongo.db.comments.remove({"_id": ObjectId(comment_id)})
    flash("Comment Successfully deleted")
    return render_template(
        "comments.html", articles=articles, post=post, comments=comments)


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):

    return render_template("500.html"), 500


if __name__ == "__main__":
    app.run(
        host=os.environ.get("IP"),
        port=int(os.environ.get("PORT")),
        debug=False)
