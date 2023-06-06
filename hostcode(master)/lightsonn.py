# import RPi.GPIO as GPIO
# import time
# import os
#
# # Set up GPIO
# GPIO.setmode(GPIO.BOARD)

import paramiko
from text import ip, po, u,word

def execute_remote_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)
    output = stdout.read().decode("utf-8").strip()
    error = stderr.read().decode("utf-8").strip()
    if error:
        print(f"Error executing command: {error}")
    else:
        print(output)



ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(ip, po, u, word)

command = 'python /home/anu/assist/fantastic-assistant-Academia-/roverML/rover/lightsoff.py'
execute_remote_command(ssh, command)



