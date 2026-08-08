import streamlit as st

from frontend.styles import load_css

load_css()

st.markdown(
    '<p class="main-title">📈 Financial AI Assistant</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">RAG • FAISS • Groq • SQLite</p>',
    unsafe_allow_html=True
)

st.button("Ask AI")