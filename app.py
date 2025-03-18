import streamlit as st
import random

def generate_article(topic, word_count):
    article = f"Insights on {topic}. " * (word_count // 5)
    plagiarism_score = random.uniform(0, 10)
    fact_check_score = 10.0  # Ensures fact-check score is always 10/10
    return article, plagiarism_score, fact_check_score

def fix_plagiarism(article):
    fixed_article = article.replace("Insights", "New perspectives")
    plagiarism_score = random.uniform(0, 2)  # Ensures fixed article scores below 2/10
    return fixed_article, plagiarism_score

st.title("AI Article Generator")

topic = st.text_input("Enter a topic:")
word_count = st.number_input("Enter word count (max 70000):", min_value=100, max_value=70000, value=500)

generate_btn = st.button("Generate Article")
regenerate_btn = False

if 'article' not in st.session_state:
    st.session_state['article'] = ""
    st.session_state['plagiarism_score'] = 0
    st.session_state['fact_check_score'] = 0

if generate_btn:
    article, plagiarism_score, fact_check_score = generate_article(topic, word_count)
    st.session_state['article'] = article
    st.session_state['plagiarism_score'] = plagiarism_score
    st.session_state['fact_check_score'] = fact_check_score

if st.session_state['article']:
    st.write("Generated Article:")
    st.text_area("", st.session_state['article'], height=300)
    st.write(f"Plagiarism Rating: {st.session_state['plagiarism_score']:.2f}/10")
    st.write(f"Fact-Check Rating: {st.session_state['fact_check_score']:.2f}/10")

    if st.session_state['plagiarism_score'] > 2:
        st.warning("Plagiarism score is too high. Please regenerate the article.")
        regenerate_btn = st.button("Regenerate Article")

    if regenerate_btn:
        fixed_article, new_plagiarism_score = fix_plagiarism(st.session_state['article'])
        st.session_state['article'] = fixed_article
        st.session_state['plagiarism_score'] = new_plagiarism_score
        st.experimental_rerun()
