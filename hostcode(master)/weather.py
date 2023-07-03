import geocoder
import requests

# Retrieve the latitude and longitude of the current location using the IP address
g = geocoder.ip('me')
latitude, longitude = g.latlng

# Retrieve the weather data for the current location using the OpenWeatherMap API
api_key = "9582519e7367d774c7644cccc7a938b1"
url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    description = data["weather"][0]["description"]
    wind_speed = data["wind"]["speed"]
    air_pressure = data["main"]["pressure"]
    temperature_kelvin = data["main"]["temp"]
    temperature_celsius = round(temperature_kelvin - 273.15)
    humidity = data["main"]["humidity"]
    print(f"Location: {g.city}, {g.state}, {g.country}")
    print(f"Surrounding is: {description}")
    print(f"Wind speed: {wind_speed} meters per second")
    print(f"Air pressure: {air_pressure} hPascals")
    print(f"Temperature: {temperature_celsius} Celsius")
    print(f"Humidity: {humidity} percent")
else:
    print("Error: Unable to retrieve weather data")