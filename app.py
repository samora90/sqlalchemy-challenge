# Import the dependencies.
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt
import pandas as pd
from flask import Flask, jsonify




#################################################
# Database Setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#################################################


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station =Base.classes.station

# Create our session (link) from Python to the DB
Session =Session(engine)

#################################################
# Flask Setup
app = Flask(__name__)
#################################################




#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    print("server for welcome page received")
    """List all available api routes."""

    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>")


@app.route("/api/v1.0/precipitation")
def precipitation():
    print("server for precipitation page received")
    most_recent_date = Session.query(func.max(measurement.date)).scalar()
    precipitation_data =(Session.query(measurement.date,measurement.prcp)
                     .filter(measurement.date >=("2016-08-23"))
                     .order_by(measurement.date)
                     .all())
    prec_data=[]
    for date, prcp in precipitation_data :
        precipitation_dict={}
        precipitation_dict["date"]=date
        precipitation_dict["prcp"]=prcp
        prec_data.append(precipitation_dict)
    return jsonify(prec_data)


@app.route("/api/v1.0/stations")
def stations():
    print("server for stations page received") 
    total_stations = Session.query(station.station).all()
    stations = list(np.ravel(total_stations))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    print("server for tobs page received")
    most_active_stations = (Session.query(measurement.station, func.count(measurement.station))
                        .group_by(measurement.station)
                        .order_by(func.count(measurement.station).desc())
                        .all())
    most_active_station = most_active_stations[0][0]
    temp_stats = Session.query(func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)).\
    filter(measurement.station == most_active_station).all()
    temp_stats = list(np.ravel(temp_stats))
    return jsonify(temp_stats)

@app.route("/api/v1.0/<start>")
def startDate(start):
    print("server for startDate page received")
    start_date = Session.query(measurement.tobs).filter(measurement.date>=start).all()
    start_date_df = pd.DataFrame(start_date)
    TMIN=start_date_df.min()
    TAVG=start_date_df.mean()
    TMAX=start_date_df.max()
    Data=[TMIN,TAVG,TMAX]
    Data = list(np.ravel(Data))
    return jsonify(Data)

@app.route("/api/v1.0/<start>/<end>")
def startDateEndDate(start,End):
    print("server for startDateEndDate page received")
    start_End_date = Session.query(measurement.tobs).filter(measurement.date>=start).\
       filter(measurement.date<=End).all()
    start_End_date_df = pd.DataFrame(start_End_date)
    TMIN=start_End_date_df.min()
    TAVG=start_End_date_df.mean()
    TMAX=start_End_date_df.max()
    Data=[TMIN,TAVG,TMAX]
    Data = list(np.ravel(Data))
    return jsonify(Data)



                    










if __name__ == '__main__':
    app.run(debug=True)