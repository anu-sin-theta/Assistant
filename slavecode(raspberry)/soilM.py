import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
#pip install adafruit-circuitpython-ads1x15------------>
# Create the I2C bus and ADC object
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)

# Create an analog input channel on the ADC
moisture_channel = AnalogIn(ads, ADS.P0)

while True:
    # Read the raw ADC value
    raw_value = moisture_channel.value

    # Map the raw value to the moisture range (0-100%)
    moisture_percent = (raw_value / 65535) * 100

    # Print the moisture level
    print('Soil Moisture: {0:.1f}%'.format(moisture_percent))

    # Wait for a few seconds before fetching the next reading.
    time.sleep(2)

