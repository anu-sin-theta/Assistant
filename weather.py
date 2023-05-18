
import geocoder
import requests

api_key = "9582519e7367d774c7644cccc7a938b1"

g = geocoder.ip('me')
latitude, longitude = g.latlng

url = f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={api_key}"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    wind_speed = data["wind"]["speed"]
    air_pressure = data["main"]["pressure"]
    temperature = data["main"]["temp"]
    humidity = data["main"]["humidity"]

    print(f"Wind speed: {wind_speed} meter per seconds")
    print(f"Air pressure: {air_pressure} hPascals")
    print(f"Temperature: {temperature} Kelvin")
    print(f"humidity: {humidity} percent")
else:
    print("Error: Unable to retrieve weather data")
