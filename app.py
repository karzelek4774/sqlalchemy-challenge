import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs"  
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of precipitation data"""
    # Query all precipitation
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date>='2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_precipitation
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict["date"] = date
        precipitation_dict["prcp"] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of dates and temperature observations of the most active station for the last year"""
    # Query all temperatures
    results = session.query(Measurement.date, Measurement.tobs)\
        .filter(Measurement.station=='USC00519281').filter(Measurement.date>='2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temperatures
    all_temperatures = []
    for date, tobs in results:
        temperatures_dict = {}
        temperatures_dict["date"] = date
        temperatures_dict["tobs"] = tobs
        all_temperatures.append(temperatures_dict)

    return jsonify(all_temperatures)


@app.route("/api/v1.0/<start>")
def temperature_start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query all temperatures
    TMIN = session.query(func.min(Measurement.tobs))\
        .filter(Measurement.date>=start).all()
    TMEAN = session.query(func.avg(Measurement.tobs))\
        .filter(Measurement.date>=start).all()
    TMAX = session.query(func.max(Measurement.tobs))\
        .filter(Measurement.date>=start).all()

    session.close()

    # Convert into normal list
    temp_start = [TMIN, TMEAN, TMAX]

    return jsonify(temp_start)


@app.route("/api/v1.0/<start>/<end>")
def temperature_start_end(start, end):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of temperature data"""
    # Query all temperature
    TMIN = session.query(func.min(Measurement.tobs))\
        .filter(Measurement.date.between(start,end)).all()
    TMEAN = session.query(func.avg(Measurement.tobs))\
        .filter(Measurement.date.between(start,end)).all()
    TMAX = session.query(func.max(Measurement.tobs))\
        .filter(Measurement.date.between(start,end)).all()

    session.close()

     # Convert into normal list
    temp_start_end = [TMIN, TMEAN, TMAX]

    return jsonify(temp_start_end)


if __name__ == '__main__':
    app.run(debug=True)