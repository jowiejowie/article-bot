import streamlit as st
from gpt4all import GPT4All
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

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
    plagiarism_score = matches / len(sentences) * 10
    return plagiarism_score

def fact_check(article):
    claims = re.findall(r'"(.*?)"', article)
    verified_claims = 0
    for claim in claims:
        results = google_search(claim)
        if results:
            verified_claims += 1
    fact_check_score = verified_claims / len(claims) * 10 if claims else 10
    return fact_check_score

def calculate_readability(article):
    words = article.split()
    sentences = article.split('.')
    syllables = sum(len(re.findall(r'[aeiouy]+', word, re.IGNORECASE)) for word in words)
    score = 206.835 - 1.015 * (len(words) / len(sentences)) - 84.6 * (syllables / len(words))
    return max(0, min(100, score))

def generate_article(topic):
    prompt = f"Write a detailed, well-structured article about {topic} with an engaging introduction and conclusion."
    article = gpt4all.generate(prompt)
    return article

def generate_headline_and_meta(article):
    prompt = f"Generate a compelling headline and meta description for this article:\n{article}"
    result = gpt4all.generate(prompt).split('\n')
    headline = result[0] if result else "Untitled Article"
    meta_description = result[1] if len(result) > 1 else "No meta description available."
    return headline, meta_description

def send_email(article, recipient):
    sender_email = "your_email@example.com"
    msg = MIMEText(article)
    msg['Subject'] = 'Your Generated Article'
    msg['From'] = sender_email
    msg['To'] = recipient
    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login(sender_email, "your_password")
        server.send_message(msg)

def main():
    st.title("AI Article Bot with GPT4All")
    topic = st.text_input("Enter a topic:")
    schedule_time = st.time_input("Schedule Posting Time (Optional)")
    email_recipient = st.text_input("Enter Email to Send Article (Optional)")

    if st.button("Generate Article"):
        article = generate_article(topic)
        headline, meta_description = generate_headline_and_meta(article)
        plagiarism_score = check_plagiarism(article)
        fact_check_score = fact_check(article)
        readability_score = calculate_readability(article)

        st.write(f"### {headline}")
        st.write(f"**Meta Description:** {meta_description}")
        st.write(article)
        st.write(f"**Plagiarism Score:** {plagiarism_score:.2f}/10")
        st.write(f"**Fact Check Score:** {fact_check_score:.2f}/10")
        st.write(f"**Readability Score:** {readability_score:.2f}/100")

        if plagiarism_score > 2:
            st.warning("High Plagiarism Score! Consider rewriting.")
            if st.button("Rewrite Article"):
                article = generate_article(topic)
                st.write(article)

        if email_recipient:
            if st.button("Send Article via Email"):
                send_email(article, email_recipient)
                st.success("Article sent successfully!")

        if schedule_time:
            st.write(f"Article scheduled to post at {schedule_time}")

if __name__ == "__main__":
    main()
