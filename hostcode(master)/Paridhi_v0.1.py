import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import subprocess
import time
import azure.cognitiveservices.speech as speechsdk
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import speech_recognition as sr
import keyboard
from database import pattern_responses
def speak(text):
    speech_config = speechsdk.SpeechConfig(subscription="855a5030c1f94d6096cda696fd25c31b", region="centralindia")
    audio_config = AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name = "en-US-SaraNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)

recognizer = sr.Recognizer()
# Set the microphone as the audio source
mic = sr.Microphone()

def recognizespeech():
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # Recognize the speech using Google Speech Recognition
    try:
        text = recognizer.recognize_google(audio)
        # print("You said: " + text)
        if not text:
            print("No speech detected. Please say it again clearly.")
        return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said. Please say it again clearly.")
    except sr.RequestError as e:
        print("Error occurred during speech recognition: {0}".format(e))

    return ""



vectorizer = TfidfVectorizer()
patterns = list(pattern_responses.keys())
pattern_vectors = vectorizer.fit_transform(patterns)


def find_similar_patterns(user_input):
    max_similarity = 0
    similar_patterns = []

    for pattern in patterns:
        pattern_vector = vectorizer.transform([pattern])
        user_vector = vectorizer.transform([user_input])
        similarity = cosine_similarity(user_vector, pattern_vector)[0][0]

        if similarity > max_similarity:
            max_similarity = similarity
            similar_patterns = [pattern]
        elif similarity == max_similarity:
            similar_patterns.append(pattern)

    return similar_patterns, max_similarity


def voice_assistant():
    while True:
        print("say robot")
        text = recognizespeech()
        if "robot" in text.lower() or "robo" in text.lower() or  keyboard.is_pressed('space')==True:
            print("Listening")
            user_input = recognizespeech()
            similar_patterns, max_similarity = find_similar_patterns(user_input)
            print("Similar patterns:", similar_patterns)

            if max_similarity > 0.5:
                responses = []
                for pattern in similar_patterns:
                    responses.extend(pattern_responses[pattern])

                response = random.choice(responses)
                print("Assistant:", response)
                speak(response)

                if 'lights' in response:
                    speak("turning on the lights")
                    output = subprocess.check_output("python lights.py", shell=True)
                    output = output.decode("utf-8").strip()
                    print(output)
                elif 'off' in response:
                    output = subprocess.check_output("python lights.py", shell=True)
                    output = output.decode("utf-8").strip()
                    print(output)
            else:
                speak("Sorry, I didn't get that. Can you please repeat?")


if __name__ == '__main__':
    voice_assistant()
