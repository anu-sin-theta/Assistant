import RPi.GPIO as GPIO 
from time import sleep 
buzz = 14       
state = GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(buzz, GPIO.OUT) 
GPIO.output(buzz, GPIO.HIGH) 
print("ON")