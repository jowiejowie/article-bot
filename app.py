import streamlit as st
import os
from gpt4all import GPT4All

# Load GPT4All model
model_path = os.path.expanduser('~') + "/AppData/Local/nomic.ai/GPT4All/Llama-3.2-1B-Instruct-Q4_0.gguf"
gpt4all = GPT4All(model_path)

def generate_article(topic, word_count):
    prompt = f"Generate a well-structured, fact-based article on {topic} with approximately {word_count} words. Ensure originality and readability."
    response = gpt4all.generate(prompt, max_tokens=word_count * 2)
    return response

def check_plagiarism(article):
    prompt = f"Analyze the following article for plagiarism and provide a plagiarism score from 0 (no plagiarism) to 10 (high plagiarism):\n{article}"
    response = gpt4all.generate(prompt)
    return float(response.strip())

def fact_check(article):
    prompt = f"Analyze the following article for factual accuracy and provide a fact-check rating from 0 (completely inaccurate) to 10 (completely accurate):\n{article}"
    response = gpt4all.generate(prompt)
    return float(response.strip())

st.title("AI-Powered Article Generator")

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
