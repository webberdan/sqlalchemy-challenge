# Set Dependencies

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# Create Engine and Set up Database

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Use automap to reflect an existing database
Base = automap_base()

# Reflecting tables into the automap
Base.prepare(engine, reflect=True)

# Set variables to call databases
station = Base.classes.station
measurement = Base.classes.measurement

# Initiate Flask 
app = Flask(__name__)

# Set Flask Routes

#Setting Homepage
@app.route("/")
def homepage():
    
    return (
        f"ALOHA, welcome to the Hawaii Weather API!<br/><br/>"
        f"Below are the available API Call Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/><br/>"
        f"/api/v1.0/2016-04-01<br/>"
        f"/api/v1.0/2016-04-01/2017-04-01<br/><br/>"
        f"Usage Intructions:<br/>"
        f"Where applicable please input the date in the following format(YYYY-MM-DD),<br/>"
        f"The start date should not be later than 2017-08-23."
    )

#Precipitation Page
@app.route('/api/v1.0/precipitation')
def precipitation():
    
    session = Session(engine)
    date_prcp = session.query(measurement.date, measurement.prcp).all()

    session.close()
    
    x = []
    for date, prcp in date_prcp:
        date_dict = {}
        date_dict[date] = prcp
        x.append(date_dict)
    return jsonify(x)

#Stations Page
@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Query the entire  station table
    station_tuple = session.query(station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(station_tuple))

    return jsonify(station_list)

#TOBS Page

@app.route('/api/v1.0/tobs')
def most_active():
    
    session = Session(engine)
    last_date = dt.date(2017,8, 23)
    query_date =  last_date - dt.timedelta(days = 365)    
    last_12_tobs = session.query(measurement.date, measurement.tobs).filter_by(station = "USC00519281").\
    filter(measurement.date >= query_date).all()

    session.close()

    last_12_list = []
    for date, tobs in last_12_tobs:
        tobs_dict = {}
        tobs_dict[date] = tobs
        last_12_list.append(tobs_dict) 
    return jsonify(last_12_list)     