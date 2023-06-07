import Adafruit_DHT

sensor = Adafruit_DHT.DHT11

pin = 4

while True:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

    if humidity is not None and temperature is not None:
        print('Temperature: {0:.1f}°C'.format(temperature))
        print('Humidity: {0:.1f}%'.format(humidity))
    else:
        print('Failed to retrieve data from sensor. Please try again.')

    time.sleep(2)
