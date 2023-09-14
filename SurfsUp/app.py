# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sulite:///Resources/hawaii.sqlite", echo=False)
session = Session(engine)

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement =  Base.classes.measurement
Station = Base.classes.station
tobs = Base.classes.tobs

# Create our session (link) from Python to the DB


#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

# List all the available routes

@app.route("/")
def index():
    return (
        f"AVAILABLE ROUTES::<br/>"
        f"<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"<br/>"
        f"/api/v1.0/stations<br/>"
        f"<br/>"
        f"/api/v1.0/tobs<br/>"
        f"<br/>"
        f"/api/v1.0/start date<br/>"
        f"<br/>"
        f"/api/v1.0/start date/end date<br/>"
        f"<br/>"
        f"<i>ENTER DATES WITH FOLLOWING FORMAT: YYYY-MM-DD</i>"
    )

# Convert the query results from your precipitation analysis 

# Return the JSON representation of your dictionary

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    query = session.query(Measurement.date,Measurement.prcp).all()
    session.close()

    precipitation = []
    for date, prcp in query:
        dict = {}
        dict["date"] = date
        dict["prcp"] = prcp
        precipitation.append(dict)
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    
    session = Session(engine)

    query = session.query(Station.name).all()
    session.close()

    stations = list(np.ravel(query))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    end_date = dt.datetime.strptime(session.query(Measurement.date)[-1:][0][0],'%Y-%m-%d')
    end_date = dt.date((end_date).year, (end_date).month, (end_date).day)
    start_date = dt.date((end_date).year-1, (end_date).month, (end_date).day)

    query = session.query(Measurement.station, func.count(Measurement.tobs)).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.tobs).desc())
    most_active_station = query[0][0]

    query = session.query(Measurement.date,Measurement.tobs).\
        filter(Measurement.station == most_active_station, Measurement.date >= start_date).all()
    session.close()

    temperature_obs = []
    for date, tobs in query:
        dict = {}
        dict["date"] = date
        dict["tobs"] = tobs
        temperature_obs.append(dict)
    return jsonify(temperature_obs)

@app.route("/api/v1.0/<start>")
def start(start):
    
    session = Session(engine)
    
    query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= f'{start}').all()
    session.close()

    temperature_obs_start = []
    for tmin, tavg, tmax in query:
        dict = {}
        dict["tmin"] = tmin
        dict["tavg"] = tavg
        dict["tmax"] = tmax
        temperature_obs_start.append(dict)
    return jsonify(temperature_obs_start)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)
    
    query = session.query(func.min(Measurement.tobs),func.avg(Measurement.tobs),func.max(Measurement.tobs)).\
        filter(Measurement.date >= f'{start}', Measurement.date <= f'{end}').all()
    session.close()

    temperature_obs_start_end = []
    for tmin, tavg, tmax in query:
        dict = {}
        dict["tmin"] = tmin
        dict["tavg"] = tavg
        dict["tmax"] = tmax
        temperature_obs_start_end.append(dict)
    return jsonify(temperature_obs_start_end)

if __name__ == '__main__':
    app.run(debug=True)