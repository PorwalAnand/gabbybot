import streamlit as st
from PIL import Image

st.set_page_config(page_title="GabbyBot", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #ffffff;
    }
    .big-button > button {
        background-color: #ff4c5b !important;
        color: white !important;
        border-radius: 12px;
        padding: 1em 2em;
        font-size: 18px;
    }
    h1, h2, h3, h4, p {
        color: #2e2e2e;
        font-family: 'Helvetica Neue', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 2])

with col1:
    image = Image.open("assets/gabby.webp")
    st.image(image, use_container_width=True)


with col2:
    st.markdown("## hi,")
    st.markdown("### I’m **gabby**")
    st.markdown("#### I’ll help you manifest a life beyond your wildest dreams")
    st.markdown("###")
    st.markdown('<div class="big-button">', unsafe_allow_html=True)
    if st.button("let’s get started"):
        st.switch_page("pages/1_Chat.py")
    st.markdown('</div>', unsafe_allow_html=True)