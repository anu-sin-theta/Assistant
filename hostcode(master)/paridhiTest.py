import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

pattern_responses = {
    ("What's up?", "How's your day?", "How are you?"): [
        "I'm doing great, thanks for asking!",
        "I'm fine, how about you?",
        "Feeling good, thank you!"
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

    return similar_patterns


def process_remembering_task(user_input):
    prefix = "remember"
    separator = None
    words = user_input.split()
    if words[0].lower() == prefix:
        for word in words:
            if word.lower() in ["is", "are", "can", "you", "please", "that", "am"]:
                separator = word
                break

    if separator:
        index = user_input.lower().index(separator.lower())
        key = user_input[len(prefix):index].strip()
        value = user_input[index + len(separator):].strip()
        pattern_responses[(key,)] = [value]
        print("Assistant: Okay, I'll remember that!")
    else:
        print("Assistant: I'm sorry, I didn't understand the remembering task.")


def voice_assistant():
    while True:
        user_input = input("User: ")

        if user_input.lower().startswith("remember"):
            process_remembering_task(user_input)
        else:
            similar_patterns = find_similar_patterns(user_input)

            if similar_patterns:
                responses = []
                for pattern in similar_patterns:
                    responses.extend(pattern_responses[pattern])

                response = random.choice(responses)
                print("Assistant:", response)
            else:
                print("Assistant: I'm sorry, I didn't understand that. Could you please rephrase?")


if __name__ == '__main__':
    voice_assistant()
