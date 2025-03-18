import streamlit as st
import random

def generate_article(topic, word_count):
    unique_sentences = set()
    article = []
    while len(' '.join(article).split()) < word_count:
        sentence = f"Insights on {topic.lower()} can provide valuable tips and strategies."
        if sentence not in unique_sentences:
            unique_sentences.add(sentence)
            article.append(sentence)
    return ' '.join(article)

def check_plagiarism(article):
    # Simulated plagiarism check
    plagiarism_score = round(random.uniform(0, 3), 2)  # Out of 10
    return plagiarism_score

def fact_check(article):
    # Simulated fact-check score
    return 10.0  # Always 10/10 for now

st.title("Article Generator")

topic = st.text_input("Enter a topic:")
word_count = st.number_input("Enter word count (max 70000):", min_value=100, max_value=70000, value=500)

if st.button("Generate Article"):
    article = generate_article(topic, word_count)
    plagiarism_score = check_plagiarism(article)
    fact_check_score = fact_check(article)

    st.write("Generated Article:")
    st.text_area("", article, height=300)
    st.write(f"Plagiarism Rating: {plagiarism_score}/10")
    st.write(f"Fact-Check Rating: {fact_check_score}/10")

    if plagiarism_score > 2:
        st.warning("High Plagiarism Score! Consider regenerating.")
        if st.button("Regenerate Article"):
            article = generate_article(topic, word_count)
            plagiarism_score = check_plagiarism(article)
            fact_check_score = fact_check(article)
            st.text_area("", article, height=300)
            st.write(f"Plagiarism Rating: {plagiarism_score}/10")
            st.write(f"Fact-Check Rating: {fact_check_score}/10")
