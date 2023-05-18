import psutil
#from theAssistant import speak
import time

cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
print(f"CPU usage: {cpu_usage}%")
print(f"Memory usage: {memory_usage}%")


