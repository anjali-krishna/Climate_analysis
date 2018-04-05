import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save reference to the table
measurement = Base.classes.Measurement
station_list = Base.classes.Station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to Climate API of Hawaii!</br>"
        f"The available API Routes are:</br>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"<bold>Specific trip data:<br/><br/></bold>"
        f"/api/v1.0/trip/\"startdate as mm-dd\"<br/>"
        f"/api/v1.0/trip/\"startdate as mm-dd\"/\"enddate as mm-dd\"<br/><br/>" 
        )


@app.route("/api/v1.0/precipitation")

def prcp_date():

    # This function returns the dates and temperature observations from the last year.
    
    prcp_measurment =session.query(measurement.date, measurement.prcp).\
    filter(measurement.date.between('2016-01-01','2016-12-31')).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    dictionary_2016_PRCP_results = dict(prcp_measurment)

    return jsonify(dictionary_2016_PRCP_results)

@app.route("/api/v1.0/stations")

def station():
    # This function returns the json list of stations from the dataset
    active_stations = session.query(station_list.station,station_list.name).all()

    # Convert the query results to a Dictionary 
    dict_stations = dict(active_stations)
    
    return jsonify(dict_stations)


@app.route("/api/v1.0/tobs")
def temp_tobs ():
    # This function returns the temperature tobs from the last year.
    
    prcp_measurment =session.query(measurement.date, measurement.tobs).\
    filter(measurement.date.between('2016-01-01','2016-12-31')).all()

    # Convert the query results to a Dictionary using date as the key and tobs as the value.
    dictionary_2016_tobs_results = dict(prcp_measurment)

    return jsonify(dictionary_2016_tobs_results)

if __name__ == '__main__':
    app.run(debug=True)
