import RPi.GPIO as GPIO
import time
import os

# Set up GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)

# Check if file exists to determine state
if os.path.isfile("gpio_state.txt"):
    with open("gpio_state.txt", "r") as file:
        state = int(file.read())
    if state == 1:
        GPIO.output(11, GPIO.LOW)
        with open("gpio_state.txt", "w") as file:
            file.write("0")
    else:
        GPIO.output(11, GPIO.HIGH)
        with open("gpio_state.txt", "w") as file:
            file.write("1")
else:
    GPIO.output(11, GPIO.HIGH)
    with open("gpio_state.txt", "w") as file:
        file.write("1")

GPIO.cleanup()
