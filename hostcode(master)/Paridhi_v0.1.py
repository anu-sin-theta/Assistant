import sys
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QLinearGradient, QPainter, QPalette
from PySide6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget
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
            return ""
        else:
            return text

    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said. Please say it again clearly.")
        return ""
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


class SpeechRecognitionThread(QThread):
    speech_input_signal = Signal(str)
    speech_recognized_signal = Signal(str)

    def run(self):
        while True:
            print("say robot")
            text = recognizespeech()
            if "robot" in text.lower() or "robo" in text.lower() or keyboard.is_pressed('space') == True:
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
                    speak("Can you please repeat?")

    def on_speech_input(self, text):
        self.speech_input_signal.emit(text)

    def on_speech_recognized(self, text):
        print("Speech recognized:", text)
        self.speech_recognized_signal.emit(text)
class ChatWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hii, I am Paridhi the Rover's AI, Type 'Voice' to activate voice mode and then say 'Robot' to activate me")
        self.setGeometry(500, 100, 700, 500)

        # Create a central widget and set it as the main window's central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Create a text edit widget to display the conversation
        self.conversation_text = QTextEdit()
        layout.addWidget(self.conversation_text)

        # Create a horizontal layout for the text input field and send button
        input_layout = QVBoxLayout()
        layout.addLayout(input_layout)

        # Create a text input field for the user to type in
        self.input_field = QTextEdit()
        self.input_field.setMaximumHeight(50)
        input_layout.addWidget(self.input_field)

        # Create a send button to send the user input to the assistant
        send_button = QPushButton("Send")
        send_button.clicked.connect(self.send_user_input)
        input_layout.addWidget(send_button)
        # Set the background gradient
        self.set_background_gradient()

        ## Create a speech recognition thread and connect its signals to slots
        self.recognition_thread = SpeechRecognitionThread()
        self.recognition_thread.speech_recognized_signal.connect(self.on_speech_recognized)
        self.recognition_thread.speech_input_signal.connect(self.on_speech_input)

    def on_speech_recognized(self, text):
        self.conversation_text.append("You: " + text)

    def on_speech_input(self, text):
        if "robot" in text.lower():
            self.recognition_thread.start()

    def send_user_input(self):
        # Get the user input from the text input field
        user_input = self.input_field.toPlainText()

        # Append the user input to the conversation text and clear the input field
        self.conversation_text.append("You: " + user_input)
        self.input_field.clear()

        if "Voice" in user_input:
            self.recognition_thread.start()
        else:
            # Get the assistant's response to the user input
            similar_patterns, max_similarity = find_similar_patterns(user_input)

            if max_similarity > 0.5:
                responses = []
                for pattern in similar_patterns:
                    responses.extend(pattern_responses[pattern])

                response = random.choice(responses)
                self.conversation_text.append("Assistant: " + response)
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
    def set_background_gradient(self):
        pal = QPalette()
        gradient = QLinearGradient(0, 0, 0, 400)
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(0, 0, 255))
        pal.setBrush(QPalette.Window, gradient)
        self.setPalette(pal)
if __name__ == '__main__':
    # Create the Qt application and the main window
    app = QApplication(sys.argv)
    window = ChatWindow()
    window.show()

    # Run the event loop
    sys.exit(app.exec())