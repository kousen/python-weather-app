import datetime
import requests
import string
import re
from flask import Flask, render_template, request, redirect, url_for
import os
from dotenv import load_dotenv
load_dotenv()

OWM_ENDPOINT = "https://api.openweathermap.org/data/2.5/weather"
OWM_FORECAST_ENDPOINT = "https://api.openweathermap.org/data/2.5/forecast"
GEOCODING_API_ENDPOINT = "https://api.openweathermap.org/geo/1.0/direct"
api_key = os.getenv("OPENWEATHERMAP_API_KEY")

app = Flask(__name__)


def get_weather_data(lat, lon, units="metric"):
    """Fetch weather data in specified unit system"""
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": units,
    }
    
    try:
        # Get current weather
        weather_response = requests.get(OWM_ENDPOINT, weather_params, timeout=5)
        weather_response.raise_for_status()
        current_weather = weather_response.json()
        
        # Get forecast
        forecast_response = requests.get(OWM_FORECAST_ENDPOINT, weather_params, timeout=5)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()
        
        return {
            'current': current_weather,
            'forecast': forecast_data,
            'units': units
        }
        
    except requests.exceptions.RequestException:
        raise Exception("Weather API request failed")


# Display home page and get city name entered into search form
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        city = re.sub(r'[^a-zA-Z\s-]', '', request.form.get("search", "").strip())
        if not city:
            return redirect(url_for("error"))
        return redirect(url_for("get_weather", city=city))
    return render_template("index.html")


# Display weather forecast for specific city using data from OpenWeather API
@app.route("/<city>", methods=["GET", "POST"])
def get_weather(city):
    # Get units from query parameter, default to metric
    units = request.args.get('units', 'metric')
    # Format city name and get current date to display on page
    city_name = string.capwords(city)
    today = datetime.datetime.now()
    current_date = today.strftime("%A, %B %d")

    # Get latitude and longitude for city
    location_params = {
        "q": city_name,
        "appid": api_key,
        "limit": 3,
    }

    try:
        location_response = requests.get(GEOCODING_API_ENDPOINT, params=location_params, timeout=5)
        location_response.raise_for_status()
        location_data = location_response.json()
    except requests.exceptions.RequestException:
        return redirect(url_for("error"))

    # Prevent IndexError if user entered a city name with no coordinates by redirecting to error page
    if not location_data:
        return redirect(url_for("error"))
    
    # If multiple cities found, let user choose
    if len(location_data) > 1:
        locations = []
        seen_coords = set()
        
        for loc in location_data:
            # Create coordinate key for deduplication
            coord_key = (round(loc['lat'], 4), round(loc['lon'], 4))
            
            # Skip if we've already seen this location
            if coord_key in seen_coords:
                continue
            seen_coords.add(coord_key)
            
            # Build display name for each location
            display_parts = [loc.get('name', city_name)]
            if 'state' in loc:
                display_parts.append(loc['state'])
            if 'country' in loc:
                display_parts.append(loc['country'])
            
            locations.append({
                'name': loc.get('name', city_name),
                'state': loc.get('state', ''),
                'country': loc.get('country', ''),
                'lat': loc['lat'],
                'lon': loc['lon'],
                'display_name': ', '.join(display_parts)
            })
        
        # If after deduplication we only have one location, go directly to it
        if len(locations) == 1:
            lat = locations[0]['lat']
            lon = locations[0]['lon']
            city_display_name = locations[0]['display_name']
        else:
            return render_template("select_city.html", locations=locations, units=units)
    else:
        # Single result - proceed as before
        location = location_data[0]
        lat = location['lat']
        lon = location['lon']
        
        # Build display name with city, state (if available), and country
        display_parts = [location.get('name', city_name)]
        if 'state' in location:
            display_parts.append(location['state'])
        if 'country' in location:
            display_parts.append(location['country'])
        city_display_name = ', '.join(display_parts)

    # Get weather data in specified units
    try:
        weather_data = get_weather_data(lat, lon, units)
    except Exception:
        return redirect(url_for("error"))

    # Extract weather data
    current_weather_data = weather_data['current']
    forecast_data = weather_data['forecast']

    # Get current weather data
    current_temp = round(current_weather_data['main']['temp'])
    current_weather = current_weather_data['weather'][0]['main']
    min_temp = round(current_weather_data['main']['temp_min'])
    max_temp = round(current_weather_data['main']['temp_max'])
    wind_speed = current_weather_data['wind']['speed']
    humidity = current_weather_data['main']['humidity']
    feels_like = round(current_weather_data['main']['feels_like'])
    
    # Get sunrise/sunset times
    sunrise_timestamp = current_weather_data['sys']['sunrise']
    sunset_timestamp = current_weather_data['sys']['sunset']
    sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
    sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')

    # Process 5-day forecast data
    five_day_temp_list = []
    five_day_weather_list = []
    
    # Extract forecast
    for item in forecast_data.get('list', []):
        if '12:00:00' in item.get('dt_txt', ''):
            if 'main' in item and 'temp' in item['main']:
                five_day_temp_list.append(round(item['main']['temp']))
            if 'weather' in item and item['weather'] and 'main' in item['weather'][0]:
                five_day_weather_list.append(item['weather'][0]['main'])
    
    # Ensure we have at least some forecast data (be more flexible)
    if len(five_day_temp_list) < 1 or len(five_day_weather_list) < 1:
        print(f"Not enough forecast data: temps={len(five_day_temp_list)}, weather={len(five_day_weather_list)}")
        return redirect(url_for("error"))
    
    # Pad lists to ensure we have 5 items (repeat last item if needed)
    while len(five_day_temp_list) < 5:
        five_day_temp_list.append(five_day_temp_list[-1] if five_day_temp_list else 0)
    while len(five_day_weather_list) < 5:
        five_day_weather_list.append(five_day_weather_list[-1] if five_day_weather_list else 'Clear')

    # Get next five weekdays to show user alongside weather data
    five_day_unformatted = [today, today + datetime.timedelta(days=1), today + datetime.timedelta(days=2),
                            today + datetime.timedelta(days=3), today + datetime.timedelta(days=4)]
    five_day_dates_list = [date.strftime("%a") for date in five_day_unformatted]

    return render_template("city.html", city_name=city_display_name, current_date=current_date, current_temp=current_temp,
                           current_weather=current_weather, min_temp=min_temp, max_temp=max_temp, wind_speed=wind_speed,
                           humidity=humidity, feels_like=feels_like, units=units, lat=lat, lon=lon,
                           sunrise_time=sunrise_time, sunset_time=sunset_time,
                           five_day_temp_list=five_day_temp_list,
                           five_day_weather_list=five_day_weather_list, five_day_dates_list=five_day_dates_list)


# Handle city selection by coordinates
@app.route("/weather", methods=["POST"])
def get_weather_by_coords():
    lat = request.form.get("lat")
    lon = request.form.get("lon")
    city_display_name = request.form.get("display_name")
    units = request.form.get("units", "metric")  # Get units from form, default to metric
    
    if not lat or not lon or not city_display_name:
        return redirect(url_for("error"))
    
    # Get current date
    today = datetime.datetime.now()
    current_date = today.strftime("%A, %B %d")
    
    # Get weather data in specified units
    try:
        weather_data = get_weather_data(lat, lon, units)
    except Exception:
        return redirect(url_for("error"))

    # Extract weather data
    current_weather_data = weather_data['current']
    forecast_data = weather_data['forecast']

    # Get current weather data
    current_temp = round(current_weather_data['main']['temp'])
    current_weather = current_weather_data['weather'][0]['main']
    min_temp = round(current_weather_data['main']['temp_min'])
    max_temp = round(current_weather_data['main']['temp_max'])
    wind_speed = current_weather_data['wind']['speed']
    humidity = current_weather_data['main']['humidity']
    feels_like = round(current_weather_data['main']['feels_like'])
    
    # Get sunrise/sunset times
    sunrise_timestamp = current_weather_data['sys']['sunrise']
    sunset_timestamp = current_weather_data['sys']['sunset']
    sunrise_time = datetime.datetime.fromtimestamp(sunrise_timestamp).strftime('%H:%M')
    sunset_time = datetime.datetime.fromtimestamp(sunset_timestamp).strftime('%H:%M')

    # Process 5-day forecast data
    five_day_temp_list = []
    five_day_weather_list = []
    
    # Extract forecast
    for item in forecast_data.get('list', []):
        if '12:00:00' in item.get('dt_txt', ''):
            if 'main' in item and 'temp' in item['main']:
                five_day_temp_list.append(round(item['main']['temp']))
            if 'weather' in item and item['weather'] and 'main' in item['weather'][0]:
                five_day_weather_list.append(item['weather'][0]['main'])
    
    # Ensure we have at least some forecast data (be more flexible)
    if len(five_day_temp_list) < 1 or len(five_day_weather_list) < 1:
        print(f"Not enough forecast data: temps={len(five_day_temp_list)}, weather={len(five_day_weather_list)}")
        return redirect(url_for("error"))
    
    # Pad lists to ensure we have 5 items (repeat last item if needed)
    while len(five_day_temp_list) < 5:
        five_day_temp_list.append(five_day_temp_list[-1] if five_day_temp_list else 0)
    while len(five_day_weather_list) < 5:
        five_day_weather_list.append(five_day_weather_list[-1] if five_day_weather_list else 'Clear')

    # Get next five weekdays to show user alongside weather data
    five_day_unformatted = [today, today + datetime.timedelta(days=1), today + datetime.timedelta(days=2),
                            today + datetime.timedelta(days=3), today + datetime.timedelta(days=4)]
    five_day_dates_list = [date.strftime("%a") for date in five_day_unformatted]

    return render_template("city.html", city_name=city_display_name, current_date=current_date, current_temp=current_temp,
                           current_weather=current_weather, min_temp=min_temp, max_temp=max_temp, wind_speed=wind_speed,
                           humidity=humidity, feels_like=feels_like, units=units, lat=lat, lon=lon,
                           sunrise_time=sunrise_time, sunset_time=sunset_time,
                           five_day_temp_list=five_day_temp_list,
                           five_day_weather_list=five_day_weather_list, five_day_dates_list=five_day_dates_list)


# Display error page for invalid input
@app.route("/error")
def error():
    return render_template("error.html")


if __name__ == "__main__":
    app.run(debug=True)