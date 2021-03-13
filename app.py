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
@app.route("/get_terms")
def get_terms():
    house_styles = list(mongo.db.house_style.find())
    return render_template("articles.html", house_styles=house_styles)


@app.route("/add_term", methods=["POST", "GET"])
def add_term():
    if request.method == "POST":
        term = {
            "term": request.form.get("term"),
            "type": request.form.get("type"),
            "usage_notes": request.form.get("usage_notes"),
        }

        mongo.db.house_style.insert_one(term)
        flash("Term successfully added")
        return redirect(url_for("get_terms"))

    house_styles = mongo.db.house_style.find().sort("house_style", 1)
    return render_template("add_term.html", house_styles=house_styles)


@app.route("/term<term_id>")
def term(term_id):
    house_style = mongo.db.house_style.find_one({"_id": ObjectId(term_id)})
    return render_template("term.html", house_style=house_style)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
