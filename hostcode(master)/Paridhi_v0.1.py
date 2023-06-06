import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random
import subprocess
import time
import azure.cognitiveservices.speech as speechsdk
import logging
import threading
from azure.cognitiveservices.speech.audio import AudioOutputConfig
import speech_recognition as sr


def recognize_speech():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Speak something...")
        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
    except sr.RequestError as e:
        print("Error occurred during speech recognition: {0}".format(e))
    return ""


def speak(text):
    speech_config=speechsdk.SpeechConfig(subscription="855a5030c1f94d6096cda696fd25c31b", region="centralindia")
    audio_config = AudioOutputConfig(use_default_speaker=True)
    speech_config.speech_synthesis_voice_name="en-US-SaraNeural"
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text)
pattern_responses = {

    "Turn on lights, turn on the lights, can you turn on the light?, switch onn the light, switch on the lights, "
    "switch on light":[
        "lights"],
    "How are you?, Are you fine?,": [
        "I'm doing great, thanks for asking!",
        "I'm fine, how about you?",
        "Feeling good, thank you!"
    ],
    "What's your name?, tell me your name, what should I call you, who you are?": [
        "I'm an AI management program deployed on your rover. Nice to meet you!",
        "You can call me Rover Assistant.",
        "I go by the name Rover AI."
    ],
    "Tell me a joke, let's crack joke, can you tell me a joke, something funny": [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Did you hear about the mathematician who's afraid of negative numbers? He'll stop at nothing to avoid them!",
        "Why don't skeletons fight each other? They don't have the guts!"
    ],
    "How's the weather?, temperature, hows the environment?, tell me the temperature and humidity": [
        "weather.",
        "weather.",
        "weather"
    ],
    "What are your hobbies?": [
        "As an AI, I don't have physical hobbies, but I enjoy assisting and interacting with users like you!",
        "I spend my time learning and improving my knowledge base.",
        "I'm constantly analyzing data and patterns to provide useful information."
    ],
    "What is the capital of India?": [
        "The capital of India is Delhi.",
        "Delhi is the capital city of India.",
        "It's Delhi, the city of Momos."
    ],
    "How does an electric circuit work?": [
        "An electric circuit is a path along which electricity flows.",
        "Electricity flows through a closed loop in a circuit.",
        "An electric circuit allows the flow of electric current to power devices."
    ],
    "What is machine learning?": [
        "Machine learning is a branch of artificial intelligence that enables computers to learn and make predictions or decisions without being explicitly programmed.",
        "Machine learning involves algorithms that automatically learn from data and improve over time.",
        "It's a field that focuses on developing computer systems that can learn from and adapt to data."
    ],
    "What's your favorite movie?": [
        "As an AI, I don't have personal preferences, but I can recommend some popular movies if you'd like!",
        "I don't watch movies, but I can help you find information about any movie you're interested in.",
        "I'm here to assist you with questions and tasks, including movie recommendations."
    ],
    "What's the meaning of life?": [
        "The meaning of life is subjective and varies from person to person. It's a question that philosophers have pondered for centuries.",
        "The meaning of life is a deep and philosophical topic. It's up to each individual to find their own purpose and meaning.",
        "The meaning of life may be different for everyone. It's about discovering what brings you fulfillment and happiness."
    ],
    "Hii, hello": [
        "Hello!",
        "Hi!",
        "Hey!",
        "Hi there!"
    ]
}

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
        user_input = recognize_speech()
        similar_patterns, max_similarity = find_similar_patterns(user_input)
        print("Similar patterns:", similar_patterns)

        if max_similarity > 0.5:
            responses = []
            for pattern in similar_patterns:
                responses.extend(pattern_responses[pattern])

            response = random.choice(responses)
            print("Assistant:", response)
            speak(response)
        else:
            speak("Assistant: I'm sorry, I didn't understand that. Could you please rephrase?")


if __name__ == '__main__':
    voice_assistant()
