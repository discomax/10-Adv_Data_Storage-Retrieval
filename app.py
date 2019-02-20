# Now that you have completed your initial analysis, design a Flask API based on the queries that you have just developed.

# Use FLASK to create your routes.

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
import numpy as np
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.station
Measurements = Base.classes.measurements 

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
def welcome():
    """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"   Precipitation data from the previous year<br/>"
        f"/api/v1.0/stations<br/>"
        f"   Weather stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"   Temp data from previous year,br/>"
        f"/api/v1.0/<start><br/>"
        f"   List of the min, avg & max temp from a given start date<br/>"
        f"/api/v1.0/<start>/<end><br/>"
        f"   List of the min, avg & max temp for a given date range data<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    year_earlier = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurements.date, Measurements.prcp).\
        filter(Measurements.date >= year_earlier).order_by(Measurements.date).all()

    # Create a list for dictionaries created from query results
    precips = []
    for result in results:
        prcp_dict = {}
        prcp_dict['date'] = result[0]
        prcp_dict['prcp'] = result[1]
        precips.append(prcp_dict)
        
    # Return the JSON representation of your dictionary
    return jsonify(precips)

@app.route("/api/v1.0/stations")
def stations(): 
    results = session.query(Station.station).all()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    year_earlier = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurements.date, Measurements.tobs).\
    filter(Measurements.date >= year_earlier).order_by(Measurements.date).all()

    # Create a list for dictionaries created from query results
    temps = []
    for result in results:
        temp_dict = {}
        temp_dict['date'] = result[0]
        temp_dict['tobs'] = result[1]
        temps.append(temp_dict)
        
    # Return the JSON representation of your dictionary
    return jsonify(temps)

@app.route("/api/v1.0/<start>")
def sDate(start):

    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).al()

    results_list = list(np.ravel(results))
    return(jsonify(results_list))

@app.route("api/v1.0/<start>/<end>")
def dateRange(start, end):

    results = session.query(func.min(Measurements.tobs), func.avg(Measurements.tobs), func.max(Measurements.tobs)).\
        filter(Measurements.date >= start).\
        filter(Measurements.date <= end).all()

    results_list = list(np.ravel(results))
    return jsonify(results_list)

if __name__ == '__main__':
    app.run(debug=True)
