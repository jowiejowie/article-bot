import streamlit as st
from gpt4all import GPT4All
import requests
from bs4 import BeautifulSoup
import re

# Load your local model with CPU mode to avoid CUDA errors
gpt4all = GPT4All("Llama-3.2-1B-Instruct-Q4_0", device="cpu")

def google_search(query, num_results=5):
    search_url = f"https://www.google.com/search?q={query}&num={num_results}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    results = [a.text for a in soup.select(".tF2Cxc .yuRUbf a")]
    return results

def check_plagiarism(article):
    sentences = article.split('.')
    matches = 0
    for sentence in sentences:
        if sentence.strip():
            results = google_search(sentence)
            if results:
                matches += 1
    plagiarism_score = matches / len(sentences) * 100
    return plagiarism_score

def fact_check(article):
    claims = re.findall(r'"(.*?)"', article)
    verified_claims = 0
    for claim in claims:
        results = google_search(claim)
        if results:
            verified_claims += 1
    fact_check_score = verified_claims / len(claims) * 100 if claims else 100
    return fact_check_score

def generate_article(topic):
    prompt = f"Write a detailed, well-structured article about {topic} with an engaging introduction and conclusion."
    article = gpt4all.generate(prompt)
    return article

def main():
    st.title("AI Article Bot with GPT4All")
    topic = st.text_input("Enter a topic:")
    if st.button("Generate Article"):
        article = generate_article(topic)
        st.write("### Generated Article")
        st.write(article)
        plagiarism_score = check_plagiarism(article)
        fact_check_score = fact_check(article)
        st.write(f"**Plagiarism Score:** {plagiarism_score:.2f}%")
        st.write(f"**Fact Check Score:** {fact_check_score:.2f}%")

if __name__ == "__main__":
    main()
