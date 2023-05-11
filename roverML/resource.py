import psutil
#from theAssistant import speak
import time

cpu_usage = psutil.cpu_percent(interval=1)
memory_usage = psutil.virtual_memory().percent
print(f"CPU usage: {cpu_usage}%")
print(f"Memory usage: {memory_usage}%")
# if cpu_usage > 90 or memory_usage > 75:
    #speak("Hiiigh resource usage detected!")
    #time.sleep(30)

