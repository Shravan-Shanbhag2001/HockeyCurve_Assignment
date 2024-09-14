from flask import Flask, request, jsonify
import requests
from apscheduler.schedulers.background import BackgroundScheduler
from Database import db_conn, init_db
from flask_cors import CORS
import datetime

app = Flask(__name__)
CORS(app)

# Initializes the database
init_db()

def get_weather():
    #Fetches data from OpenWeather for the supported locations only
    locations = ["New Delhi", "Mumbai", "Chennai", "Bengaluru", "Kolkata"] 
    api_key = '790eef091c61cfd70a5bd9c0e5dcdc2c'

    for location in locations:
        api_url = 'https://api.openweathermap.org/data/2.5/weather'
        querystring = {
            "q": location,
            "appid": api_key,
            "units": "metric"
        }
        
        response = requests.get(api_url, params=querystring)
        print(response.url)

        if response.status_code == 200:
            data = response.json()

            #Parsing the relevant JSON content and storing it
            timestamp = datetime.datetime.utcfromtimestamp(data['dt']).strftime('%Y-%m-%d %H:%M:%S')
            location_name = data['name']
            country = data['sys']['country']
            temperature = data['main']['temp']
            temp_min = data['main']['temp_min']
            temp_max = data['main']['temp_max']
            weather_icons = data['weather'][0]['icon']
            weather_descriptions = data['weather'][0]['description']
            wind_speed = data['wind']['speed']
            wind_degree = data['wind']['deg']
            pressure = data['main']['pressure']
            humidity = data['main']['humidity']
            cloudcover = data['clouds']['all']
            feelslike = data['main']['feels_like']
            visibility = data['visibility']
            rain = data.get('rain', {}).get('1h', 0)

            #Connecting to database and populating the table in it with data
            conn = db_conn()
            conn.execute('''INSERT INTO weather_data (
                timestamp, location, country, temperature, temp_min, temp_max, weather_icons,
                weather_descriptions, wind_speed, wind_degree, pressure,
                humidity, cloudcover, feelslike, visibility, rain)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (timestamp, location_name, country, temperature, temp_min, temp_max, weather_icons,
                weather_descriptions, wind_speed, wind_degree, pressure,
                humidity, cloudcover, feelslike, visibility, rain)
            )

            conn.commit()
            conn.close()

#Dummy endpoint so ignore
@app.route('/')
def index():
    return 'Welcome!'

#Endpoint that takes GET request from frontend and sends back the requested response
@app.route('/get-current-weather-data', methods=['GET'])
def send_data():
    location = request.args.get('location')
    
    if not location:
        return jsonify({"error": "Location parameter is required"}), 400
    
    conn = db_conn()
    
    query = '''
        SELECT timestamp, location, country, temperature, temp_max, temp_min, weather_icons,
               weather_descriptions, wind_speed, wind_degree, pressure,
               humidity, cloudcover, feelslike, visibility, rain
        FROM weather_data
        WHERE location = ?
        ORDER BY timestamp DESC
        LIMIT 1
    '''
    data = conn.execute(query, (location,)).fetchone()
    
    if data is None:
        return jsonify({"error": "No data found for the specified location"}), 404
    
    result = dict(data)
    
    return jsonify(result)

#Endpoint for sending historical data for analysis
@app.route('/get-range_weather-data', methods=['GET'])
def get_range_weather_data():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    # Convert dates to ISO format
    start_timestamp = datetime.datetime.strptime(start_date, '%d-%m-%Y').date()
    end_timestamp = datetime.datetime.strptime(end_date, '%d-%m-%Y').date()

    conn = db_conn()
    
    # Modify the query to compare only the date part
    query = """
    SELECT DATE(timestamp) as date, temperature, humidity, feelslike, pressure
    FROM weather_data
    WHERE DATE(timestamp) BETWEEN ? AND ?
    """
    
    rows = conn.execute(query, (start_timestamp, end_timestamp)).fetchall()
    
    if rows:
        data = [dict(zip(['date', 'temperature', 'humidity','feelslike','pressure'], row)) for row in rows]
        return jsonify(data)
    else:
        return jsonify([]), 204

if __name__ == '__main__':
    #Scheduler which runs the get_weather function every 1 hour (when server is on) 
    #So that data is fetched periodically
    scheduler = BackgroundScheduler()
    scheduler.add_job(get_weather, 'interval', hours=1)
    scheduler.start()
    
    get_weather()
    
    print("Scheduler started")
    app.run(debug=False, use_reloader=False)
