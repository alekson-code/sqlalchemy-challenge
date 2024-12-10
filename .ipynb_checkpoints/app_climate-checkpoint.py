from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create an app instance
app = Flask(__name__)

# ######################################################
# # Configure the SQLite database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hawaii.sqlite'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Initialize the database
# db = SQLAlchemy(app)

# # Reflect the database schema
# Base = automap_base()
# Base.prepare(db.engine, reflect=True)

# ######################################################

# Save references to the tables
Measurement = Base.classes.measurement
Station = Base.classes.station

# # Create a session
# session = Session(db.engine)

# Define the landing page route
@app.route('/')
def home():
    return "Welcome to the Hawaii Climate API!"

# Create a session
session = Session(engine)

# Define a route to display available routes
@app.route('/api/v1.0/routes')
def routes():
    return jsonify({
        'routes': [
            '/',
            '/api/v1.0/measurements',
            '/api/v1.0/stations'
        ]
    })

# Run the server
if __name__ == '__main__':
    app.run(debug=True)