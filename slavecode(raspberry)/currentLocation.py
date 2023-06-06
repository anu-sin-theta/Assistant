#from gpiozero import GPS
import requests
import folium
import os
import webbrowser
#gps = GPS()

def get_location_name(lat, lon):
    try:
        response = requests.get(f"https://api.opencagedata.com/geocode/v1/json?q={lat}+{lon}&key=1965fd0c81064409b2a74a13d4264ec7")
        response_json = response.json()

        location_name = response_json['results'][0]['formatted']
    except requests.exceptions.RequestException:
        location_name = "Sorry, there was an error. Please try again later."
    return location_name

# Get current location
#gps.wait_for_fix()
lat = 27.6058  # gps.latitude
lon = 77.5934  # gps.longitude

# Get location name
location_name = get_location_name(lat, lon)

# Create map centered on current location
m = folium.Map(location=[lat, lon], zoom_start=13)

# Add marker at current location
folium.Marker([lat, lon], popup=location_name).add_to(m)

# Display map
m.save("roverLocation.html")
webbrowser.open("roverLocation.html")
print(f"Current latitude: {lat:.6f}")
print(f"Current longitude: {lon:.6f}")
print(f"Current location: {location_name}")
