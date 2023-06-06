import geocoder

# Get current latitude and longitude
g = geocoder.ip('me')
latitude, longitude = g.latlng

# Print latitude and longitude
print(f"Latitude: {latitude}")
print(f"Longitude: {longitude}")
