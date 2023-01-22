# Exploring and Analyzing Hawaii Weather Data using Python, SQLAlchemy and Flask

This is a project that uses Python, SQLAlchemy, and Flask to explore and analyze weather data from Hawaii. The project includes the following components:
Data Extraction: The project uses SQLAlchemy to connect to a SQLite database that contains weather data for Hawaii. The data is read from csv files and loaded into the database.

## Data Exploration
The project uses SQLAlchemy and Pandas to explore and analyze the weather data. The script performs various queries to retrieve and plot precipitation data, temperature data, and station data.

## Flask API
The project uses Flask to create a RESTful API that allows users to access the weather data in JSON format. The API includes routes for precipitation data, temperature data, and station data.

## Requirements
- Python 3.6 or later
- Flask
- SQLAlchemy
- Pandas
- Matplotlib

## Usage
- Clone the repository
- Navigate to the project directory
- Install the requirements
- Run the script: flask run
- The API will be available at http://localhost:5000/

## API Routes
- /: Homepage that lists all the available routes.
- /api/v1.0/precipitation: Returns the precipitation data for the last 12 months in JSON format.
- /api/v1.0/stations: Returns a list of all the stations in the dataset in JSON format.
- /api/v1.0/tobs: Returns the temperature observations for the most active station for the last year in JSON format.
- /api/v1.0/<start>: Returns the minimum, average, and maximum temperature for a specified start date.
- /api/v1.0/<start>/<end>: Returns the minimum, average, and maximum temperature for a specified start-end date range.

## Note
- In case of any issues, please check the log for more information, you can add the following line app.run(debug=True) before if __name__ == '__main__': it will give you more information about the error
- If you're still facing the issue, please provide more details about the error message you're seeing and the versions of the packages you're using.

## References
- Menne, M.J., I. Durre, R.S. Vose, B.E. Gleason, and T.G. Houston, 2012: An overview of the Global Historical Climatology Network-Daily Database. Journal of Atmospheric and Oceanic Technology, 29, 897-910, https://doi.org/10.1175/JTECH-D-11-00103.1 Links to an external site., measurements converted to metric in Pandas.
