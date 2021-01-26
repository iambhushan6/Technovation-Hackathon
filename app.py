
from flask import Flask,render_template,request,jsonify,redirect
# import util
import os

import jinja2
import json
import pickle
import numpy as np
app = Flask(__name__)

__location = None
__data_columns = None
__model = None

def get_predicted_price(location,sqft,bhk,bath):
    global __data_columns
    try:
        loc_index = __data_columns.index(location.lower())
    except:
        loc_index = 154
    x = np.zeros(len(__data_columns))
    x[0] = sqft
    x[1] = bath
    x[2] = bhk
    if loc_index >= 0:
        x[loc_index] = 1
    return round(__model.predict([x])[0],2)

def getlocations():
    return __location

def get_location_and_model():
    # print("Loading locations n price")
    global __data_columns
    global __location
    global __model

    with open("columns.json","rb") as f:
        __data_columns = json.load(f)['data_columns']
        __location = __data_columns[3:]
    f.close()

    with open("banglore_home_prices_model.pickle","rb") as f:
        __model = pickle.load(f)
    f.close()

getlocations()
get_location_and_model()

@app.route("/")
def home():
    return render_template("index.html",locations = __location)

@app.route("/", methods=["POST"])
def predict():
    if request.method == "POST":
        location = request.form['location']
        sqft = request.form['sqft']
        bath = request.form['bath']
        bhk = request.form['bhk']

        price = float(get_predicted_price(location,sqft,bath,bhk))
        price_per_sqft= round((float(float(price)/int(sqft)))*100000,2)
        # locations = __location
    return render_template("index.html", predicted_price  = price, locations = __location,
                           price_sqft=price_per_sqft, checked_location=location)




app.run(debug=True)
