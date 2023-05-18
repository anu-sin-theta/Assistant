import os
import subprocess
import time
import azure.cognitiveservices.speech as speechsdk
import logging
import threading
from azure.cognitiveservices.speech.audio import AudioOutputConfig
from speech_recognition import UnknownValueError

serpapi_endpoint = "https://serpapi.com/search?engine=bing"
serpapi_key = "89cccdeec194d9823309de02183781929bfd677560482ef1a689b1bc643ffc5c"


def speak(text):
    speech_config=speechsdk.SpeechConfig(subscription="35fd61e5aea43178765f37173d07686", region="centralindia")
    audio_config = AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name="en-US-SaraNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

# def get_bing_answer(query):
#     try:
#         params = {
#             "engine": "bing",
#             "q": query,
#             "api_key": serpapi_key,
#             "output": "json"
#         }
#
#         response = requests.get(serpapi_endpoint, params=params)
#
#         response_json = response.json()
#
#         answer = response_json["organic_results"][0]["snippet"]
#
#         message = f"The answer to your question is: {answer}"
#     except (requests.exceptions.RequestException, IndexError, KeyError):
#         message = "Sorry, I'm not sure about that. Please try asking me something else."
#     return message
def get_logs():
    while True:
        weather_output = subprocess.check_output("python weather.py", shell=True)
        weather_output = weather_output.decode("utf-8").strip()
        resource_output = subprocess.check_output("python resource.py", shell=True)
        resource_output = resource_output.decode("utf-8").strip()
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S")
        with open("weather.log", "a") as weather_log:
            weather_log.write(f"{current_time} - {weather_output}\n")
        with open("resource.log", "a") as resource_log:
            resource_log.write(f"{current_time} - {resource_output}\n")
        time.sleep(30)
        data = "Data gathered at {}".format(time.time())
        with open('my_log_file.log', 'a') as f:
            f.write(data + '\n')

        time.sleep(60)


log_thread = threading.Thread(target=get_logs)


def voice_assistant():
    speak("Hii my name is Mily your  voice assistant, how can i help you with? you may just try asking me.")
    while True:
        speech_config = speechsdk.SpeechConfig(subscription="35fd61e5aea43178765f37173d07686", region="centralindia")
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        result = speech_recognizer.recognize_once_async().get()

        try:
            text = result.text
            print("#AnuFied -CSED")
            if "how is the weather" in text or "what how's the weather" in text \
                    or "tell me the weather" in text or "give me the weather update" in text or "current weather" in text or "current weather update"in text:
                speak("Fetching data")
                output = subprocess.check_output("python weather.py", shell=True)
                output = output.decode("utf-8").strip()
                print(output)
                speak(output)
            elif 'turn on lights' in text or "it's too dark" in text or "turn off lights" in text:
                speak("Alright captain")
                output = subprocess.check_output("python lights.py", shell=True)
                output = output.decode("utf-8").strip()
                print(output)
                speak(output)
            elif 'what is the location' in text or "tell me your coordinates" in text or "current location" in text or "coordinates"in text or "What is the current location"in text:
                speak("Fetching location")
                output = subprocess.check_output("python currentLocation.py", shell=True)
                output = output.decode("utf-8").strip()
                print(output)
                speak(output)

            elif "what's the ram and cpu usage" in text or "Tell me the cpu usage" in text or "system usage" in text  or " current cpu usage"in text or "system load"in text or "Current ram cpu usage" in text or "memory usage"in text:

                speak("Asking CPU")
                output = subprocess.check_output("python resource.py", shell=True)
                output = output.decode("utf-8").strip()
                print(output)
                time.sleep(0.6)
                speak(output)
            elif "start logging" in text or "initiate logging" in text:
                speak("sure, I've started collecting logs.")
                log_thread.start()

            elif "weather logs" in text:
                speak("Fetching weather logs...")
                subprocess.check_output("weather.log", shell=True)
                time.sleep(2)
                speak("Here are the recent logs for environmental data")

            elif "resource logs" in text:
                speak("Fetching resource logs...")
                subprocess.check_output("resource.log", shell=True)
                time.sleep(2)
                speak("Here are the recent logs for system data!")

        except UnknownValueError:
            speak("I didn't get that. Can you please repeat?")


if __name__ == '__main__':
    while True:
        voice_assistant()


