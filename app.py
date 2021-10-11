from flask import Flask
from fastapi import FastAPI
from flask import Flask, render_template, url_for, redirect
from flask.helpers import flash
from flask.wrappers import Response
from forms import DunkerForm
from pymongo import MongoClient, collection
import json
from dotenv import dotenv_values
import random

config = dotenv_values(".env")
app = Flask(__name__)
app.config["SECRET_KEY"] = config["SECRET_KEY"]
HOST = config["HOST"]
client = MongoClient(HOST)


@app.route("/", methods=["GET", "POST"])
def index():
    form = DunkerForm()
    if form.validate_on_submit():
        dunker_name = form.name.data
        return redirect(url_for("dunker_view", dunker_name=dunker_name))
    else:
        pass
    return render_template("index.html", form=form)

@app.route("/_autocomplete", methods=["GET"])
def autocomplete():
    db = client["DunkerDB"]
    collection = db["dunkers"]
    dunker_cursor = collection.find({"Name":{"$exists": True}})
    names = [document["Name"] for document in dunker_cursor] 
    return Response(json.dumps(names), mimetype="application/json")

@app.route("/dunkers/<dunker_name>", methods=["GET", "POST"])
def dunker_view(dunker_name):
    db = client["DunkerDB"]
    collection = db["dunkers"]
    dunker = collection.find_one({"Name": dunker_name})
    if dunker is not None:
        flash(f"Dunker: {dunker_name} Found!", "success")
        return render_template("dunkerview.html", dunker=dunker)
    else:
        flash(f"Dunker: {dunker_name} Not Found", "warning")
        return redirect(url_for("index"))

@app.route("/random")
def random_dunker():
    db = client["DunkerDB"]
    collection = db["dunkers"]
    dunker_cursor = collection.find({"Name":{"$exists": True}})
    names = [document["Name"] for document in dunker_cursor]
    random_num = random.randint(0, len(names))
    random_dunker = collection.find_one({"Name": names[random_num]})
    # random_dunker = collection.aggregate([{'$sample': {'size': 1 }}], batchSize=1)
    return redirect(url_for("dunker_view", dunker_name=random_dunker["Name"]))

if __name__ == "__main__":
    app.run(debug=True)
