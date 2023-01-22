from flask import Flask, jsonify
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

# # Reflect Tables into SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
stations_df = pd.read_csv('Resources/hawaii_stations.csv')
measurements_df = pd.read_csv('Resources/hawaii_measurements.csv')
# load the dataframe into the in-memory sqlite db
stations_df.to_sql('stations', engine, if_exists='replace')
measurements_df.to_sql('measurements', engine, if_exists='replace')

# reflect the tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# View all of the classes that automap found
print(Base.classes.keys())

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(bind=engine)

# # Exploratory Precipitation Analysis

# Find the most recent date in the data set.
most_recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
print(most_recent_date)

# Design a query to retrieve the last 12 months of precipitation data and plot the results. 
# Starting from the most recent data point in the database. 
# Calculate the date one year from the last date in data set
last_year_date = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

# Perform a query to retrieve the data and precipitation scores
precipitation_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= last_year_date).\
    order_by(Measurement.date).all()

# Save the query results as a Pandas DataFrame
precipitation_df = pd.DataFrame(precipitation_data, columns=['date', 'precipitation'])

# Set the index to the date column
precipitation_df.set_index('date', inplace=True)

# Sort the dataframe by date
precipitation_df.sort_index(inplace=True)

# Use Pandas Plotting with Matplotlib to plot the data
fig, ax = plt.subplots()
precipitation_df.plot(ax=ax, title="Precipitation (last 12 months)")
ax.set_xlabel("Date")
ax.set_ylabel("Precipitation")
ax.set_xticklabels(precipitation_df.index, rotation=90)
plt.show()

# Use Pandas to calcualte the summary statistics for the precipitation data
print(precipitation_df.describe())

# # Exploratory Station Analysis

# Design a query to calculate the total number stations in the dataset
total_stations = session.query(func.count(Station.id)).scalar()
print(total_stations)

# Design a query to find the most active stations (i.e. what stations have the most rows?)
# List the stations and the counts in descending order.
most_active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()
print(most_active_stations)

# Using the most active station id from the previous query, calculate the lowest, highest, and average temperature.
most_active_station = most_active_stations[0][0]

lowest_temp = session.query(func.min(Measurement.tobs)).filter(Measurement.station == most_active_station).scalar()
highest_temp = session.query(func.max(Measurement.tobs)).filter(Measurement.station == most_active_station).scalar()
average_temp = session.query(func.avg(Measurement.tobs)).filter(Measurement.station == most_active_station).scalar()
print(f"Lowest temperature: {lowest_temp}")
print(f"Highest temperature: {highest_temp}")
print(f"Average temperature: {average_temp}")

# Using the most active station id
# Query the last 12 months of temperature observation data for this station and plot the results as a histogram
# Calculate the date one year from the last date in data set
last_year_date = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

# Perform a query to retrieve the data and temperature scores
temperature_data = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= last_year_date).\
    filter(Measurement.station == most_active_station).\
    order_by(Measurement.date).all()

# Plot the temperature data as a histogram
temperature_df = pd.DataFrame(temperature_data, columns=['date', 'temperature'])
temperature_df.plot.hist(bins=12)
plt.xlabel("Temperature")
plt.show()

session.close()

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Climate Analysis API! Available routes: /api/v1.0/precipitation, /api/v1.0/stations, /api/v1.0/tobs, /api/v1.0/<start>, /api/v1.0/<start>/<end>"

@app.route("/api/v1.0/precipitation")
def precipitation():
    last_year_date = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= last_year_date).\
        order_by(Measurement.date).all()

    precipitation = {date: prcp for date, prcp in precipitation_data}
    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    stations_data = session.query(Station.station).all()
    stations = list(np.ravel(stations_data))
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    last_year_date = datetime.strptime(most_recent_date, '%Y-%m-%d') - timedelta(days=365)

    temperature_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.date >= last_year_date).\
        filter(Measurement.station == most_active_station).\
        order_by(Measurement.date).all()

    temperature = list(np.ravel(temperature_data))
    return jsonify(temperature)

@app.route("/api/v1.0/<start>")
def temp_start(start):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).all
    temp = list(np.ravel(temp_data))
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def temp_start_end(start, end):
    temp_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temp = list(np.ravel(temp_data))
    return jsonify(temp)

if __name__ == "__main__":
    app.run(debug=True)
