import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify
app = Flask(__name__)

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Measurement = Base.classes.measurement
Station = Base.classes.station

@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    all_measurement = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict["date"] = date
        measurement_dict["prcp"] = prcp
        all_measurement.append(measurement_dict)

    return jsonify(all_measurement)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    
    results = session.query(Station.station).all()

    session.close()

    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
# couldn't get this to run
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').filter(Measurement.station == 'USC00519281')

    session.close()

    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)


# Not sure how to complete these two routes
@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)

    # canonicalized = start.replace(" ", "").lower()
    # for date in Measurement.date:
    #     search_term = date["start"].replace(" ", "").lower()

    #     if search_term == canonicalized:
    #         return jsonify(results)

    # return jsonify({"error": f"Start date {start} not found."}), 404

    # results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= start)
   
    session.close()

    return jsonify(results)

@app.route("/api/v1.0/<start>/<end>")
def end_date(end):
    session = Session(engine)

    session.close()

    return jsonify()


if __name__ == '__main__':
    app.run(debug=True)