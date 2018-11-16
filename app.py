import datetime as dt
import numpy as np
import pandas as pd
import datetime as dt
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()

Base.prepare(engine, reflect=True)

Station = Base.classes.station

session = Session(engine)

app = Flask(__name__)

@app.route('/')
def welcome():
    return jsonify({"Title": "Hawaii weather info app",
    	"description": "This api gives you the information about Hawaii stations, precipitation and temperature in a daterange",
    	"endpoints":["/api/v1.0/precipitation",
    	"/api/v1.0/stations",
    	"/api/v1.0/tobs",
    	"/api/v1.0/<start>",
    c	"/api/v1.0/<start>/<end>"]})


@app.route('/api/v1.0/stations')
def stations():
    query = 'SELECT station, name FROM stations'
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));


@app.route('/api/v1.0/<start>')
def temps_startOnly(start):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
             AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
             FROM measurements WHERE date >= "{start}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records'));



@app.route('/api/v1.0/<start>/<end>')
def temps_startAndEnd(start, end):
    query = (f'SELECT AVG(temp) AS "Average Temperature", MIN(temp) \
             AS "Minimum Temperature", MAX(temp) AS "Maximum Temperature" \
             FROM measurements WHERE date >= "{start}" AND date <= "{end}"')
    return jsonify(pd.read_sql(query, engine).to_dict(orient='records')); 

if __name__ == '__main__':
    app.run(debug=True)