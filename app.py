import streamlit as st
from googlesearch import search
import random

def generate_article(topic, word_count):
    article = f"This is a {word_count}-word article about {topic}.\n"
    for _ in range(word_count // 10):
        article += f"More insights on {topic}. "
    return article

def fact_check_article(article):
    results = search(article, num_results=5)
    fact_check_rating = random.uniform(0.7, 1.0)  # Simulating fact-check rating
    return fact_check_rating, results

def check_plagiarism(article):
    results = search(article, num_results=5)
    plagiarism_rating = random.uniform(0.0, 0.5)  # Simulating plagiarism rating
    return plagiarism_rating, results

def rewrite_article(article):
    sentences = article.split('. ')
    rewritten = ' '.join(random.sample(sentences, len(sentences)))
    return rewritten

st.title('Article Generator Bot')

# User input
article_topic = st.text_input('Enter a topic:', '')
word_count = st.number_input('Enter word count (max 70000):', min_value=100, max_value=70000, value=500)

if st.button('Generate Article'):
    if article_topic:
        article = generate_article(article_topic, word_count)
        plagiarism_rating, _ = check_plagiarism(article)
        fact_check_rating, _ = fact_check_article(article)

        if plagiarism_rating > 0.1:
            st.write('Plagiarism detected. Article rewritten to avoid plagiarism.')
            article = rewrite_article(article)
        
        st.text_area('Generated Article:', article, height=300)
        st.write(f'Plagiarism Rating: {plagiarism_rating:.2f}')
        st.write(f'Fact-Check Rating: {fact_check_rating:.2f}')
    else:
        st.error('Please enter a topic.')
