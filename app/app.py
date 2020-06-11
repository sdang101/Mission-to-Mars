from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection

# Connect app to Mongo using URI (uniform resource identifier)
# URI says the app can reach Mongo through our localhost server, using port 27017,
# using a database named mars_app”.
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Set Up App Routes
@app.route("/")
def index():
    # Use PyMongo to find the 'mars' collection in our database
    mars = mongo.db.mars.find_one()
    # Tell Flask to return an HTML template using an index.html file
    return render_template("index.html", mars=mars) # Tells Python to use the 'mars' collection in MongoDB

# Set Scraping Route
@app.route("/scrape")
def scrape():
    # Assign variable mars to point to our Mongo database
    mars = mongo.db.mars
    # Assign variable mars_data to hole newly scraped data
    mars_data = scraping.scrape_all()
    # Update the database, tell Mongo to create a new document if one doesn't exist
    mars.update({}, mars_data, upsert=True)
    return redirect('/',code=302)

if __name__ == '__main__':
    app.run(debug=True)