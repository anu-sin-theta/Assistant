import requests
from bs4 import BeautifulSoup
from googlesearch import search
from gensim.summarization import summarize

query = "python tutorial"
url = None

for result in search(query, num_results=1):
    url = result
    break

if url:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text()
    summary = summarize(text, ratio=0.2)
    print(summary)
else:
    print("No results found for the given query.")
