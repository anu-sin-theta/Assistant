
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
# import paramiko
# from text import ip, po, u,word
#
# def execute_remote_command(ssh, command):
#     stdin, stdout, stderr = ssh.exec_command(command)
#     output = stdout.read().decode("utf-8").strip()
#     error = stderr.read().decode("utf-8").strip()
#     if error:
#         print(f"Error executing command: {error}")
#     else:
#         print(output)
#
#
#
# ssh = paramiko.SSHClient()
# ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
# ssh.connect(ip, po, u, word)
#
# command = 'python /home/anu/assist/fantastic-assistant-Academia-/roverML/rover/weather.py'
# execute_remote_command(ssh, command)


