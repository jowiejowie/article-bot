import streamlit as st
from googlesearch import search
import random
import time

def generate_article(topic, word_count):
    paragraphs = ["""
    In the realm of {}, countless opportunities unfold as technology evolves. Entrepreneurs and businesses explore new frontiers, harnessing the power of innovation to reshape industries and redefine possibilities.
    """.format(topic)] * (word_count // 100)
    article = "\n\n".join(paragraphs)[:word_count]
    return article

def fact_check(article):
    queries = article.split(". ")[:5]  # Limit queries to avoid getting blocked
    fact_check_score = 100
    for query in queries:
        try:
            results = list(search(query, num_results=5))
            if len(results) < 2:
                fact_check_score -= 20
        except Exception as e:
            fact_check_score -= 20
    return fact_check_score

def plagiarism_check(article):
    queries = article.split(". ")[:5]
    plagiarism_score = 0
    for query in queries:
        try:
            results = list(search(query, num_results=5))
            if results:
                plagiarism_score += 20
        except Exception as e:
            pass
    return plagiarism_score

def rewrite_article(article):
    sentences = article.split(". ")
    rewritten_sentences = [sentence[::-1] for sentence in sentences]  # Simple reverse for demonstration
    return ". ".join(rewritten_sentences)

st.title("Article Bot")

topic = st.text_input("Enter a topic:")
word_count = st.number_input("Enter word count (max 70000):", min_value=100, max_value=70000, value=1000)

if st.button("Generate Article"):
    article = generate_article(topic, word_count)
    fact_check_score = fact_check(article)
    plagiarism_score = plagiarism_check(article)
    
    if plagiarism_score > 50:
        article = rewrite_article(article)
        st.write("Plagiarism detected. Article rewritten to avoid plagiarism.")
    
    st.write(article)
    st.write(f"Fact-Check Rating: {fact_check_score}%")
    st.write(f"Plagiarism Rating: {plagiarism_score}%")
