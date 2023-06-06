import openai

openai.api_key = "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"


response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a chatbot"},
            {"role": "user", "content": "Gla CSED?"},
        ]
)

result = ''
for choice in response.choices:
    result += choice.message.content

print(result)