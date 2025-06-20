# main.py
import streamlit as st
from frontend.chat_interface import academic_chatbot
from frontend.layout import custom_styling, show_header

st.set_page_config(page_title="ParaScope", layout="wide", page_icon="📘")
custom_styling()
show_header()
academic_chatbot()
