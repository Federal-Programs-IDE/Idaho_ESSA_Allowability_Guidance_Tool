import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(layout="wide")

# Load and display your exact HTML file
with open("grant_lookup_tool.html", "r", encoding="utf-8") as f:
    html_code = f.read()

components.html(html_code, height=900, scrolling=True)
