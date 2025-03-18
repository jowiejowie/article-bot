import streamlit as st

# Title of your app
st.title("Article Bot")

# Input box for the topic
topic = st.text_input("Enter a topic:")

# Button to generate article
if st.button("Generate Article"):
    article = f"This is a sample article about {topic}."
    st.write(article)

# Button to download article
if article:
    st.download_button("Download Article", article, "article.txt")
