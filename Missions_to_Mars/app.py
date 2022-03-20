from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars


app = Flask(__name__)


mongo = PyMongo(app, uri = "mongodb://localhost:27017/mission_mars_db")


@app.route("/")
def index():
    mission_mars_data = mongo.db.information.find_one()
    return render_template("index.html", mission_mars_data = mission_mars_data)


@app.route("/scrape")
def scrape():
    mission_mars_data = scrape_mars.scraper()
    mongo.db.information.update_one({}, {"$set" : mission_mars_data}, upsert = True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
