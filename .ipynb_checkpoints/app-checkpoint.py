#==============================================================================================
#Climate App Design
# Create Your Flask App
# Create a new Python file, for example, app.py, and set up your Flask application as follows:

#===Install Flask SQLAlchemy if necessary =====================================================
#pip install Flask SQLAlchemy
#==============================================================================================
# Import Dependencies
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
import datetime as datetime

#==============================================================================================
#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hawaii.sqlite'
# db = SQLAlchemy(app)

# # Reflect the database schema
# Base = automap_base()
# Base.prepare(db.engine, reflect=True)

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

@app.route('/')
def home():
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Query for the last 12 months of precipitation data
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()
    
    # Create a dictionary from the results
    precipitation_data = {date: prcp for date, prcp in results}
    return jsonify(precipitation_data)

@app.route('/api/v1.0/stations')
def stations():
    # Query for all stations
    results = session.query(Station.station).all()
    stations_list = [station[0] for station in results]
    return jsonify(stations_list)

@app.route('/api/v1.0/tobs')
def tobs():
    # Query for the most active station's temperature observations for the last year
    last_year = datetime.datetime.now() - datetime.timedelta(days=365)
    results = session.query(Measurement.tobs).filter(Measurement.date >= last_year, Measurement.station == 'USC00519281').all()
    temp_observations = [temp[0] for temp in results]
    return jsonify(temp_observations)

@app.route('/api/v1.0/<start>')
def start(start):
    # Query for min, avg, and max temperatures from the start date to the latest date
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).all()
    
    temps = list(results[0])
    return jsonify({
        'TMIN': temps[0],
        'TAVG': temps[1],
        'TMAX': temps[2]
    })

@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    # Query for min, avg, and max temperatures between start and end dates
    results = session.query(
        func.min(Measurement.tobs),
        func.avg(Measurement.tobs),
        func.max(Measurement.tobs)
    ).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    
    temps = list(results[0])
    return jsonify({
        'TMIN': temps[0],
        'TAVG': temps[1],
        'TMAX': temps[2]
    })

if __name__ == '__main__':
    app.run(debug=True)