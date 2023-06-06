# import psutil
# #from theAssistant import speak
# import time
#
# cpu_usage = psutil.cpu_percent(interval=1)
# memory_usage = psutil.virtual_memory().percent
# print(f"CPU usage: {cpu_usage}%")
# print(f"Memory usage: {memory_usage}%")
# # if cpu_usage > 90 or memory_usage > 75:
#     #speak("Hiiigh resource usage detected!")
#     #time.sleep(30)
import paramiko
from text import ip, po, u, word

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

command = 'python /home/anu/assist/fantastic-assistant-Academia-/roverML/rover/theresource.py'
execute_remote_command(ssh, command)


