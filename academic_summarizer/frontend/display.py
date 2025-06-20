# frontend/display.py
import streamlit as st

def summarization_mode_selector():
    return st.radio("Select Summarization Mode", [
        "Summary",
        "Summary + Glossary",
        "Only Glossary",
        "Full (Summary + Glossary + Analysis Q/A)"
    ], key="summary_mode")

def text_input_ui():
    text = st.text_area(" Paste your academic text here", height=300)
    mode = summarization_mode_selector()
    return text, mode

def pdf_input_ui():
    file = st.file_uploader("  Upload a PDF file", type=["pdf"])
    mode = summarization_mode_selector()
    return file, mode

def image_input_ui():
    image = st.file_uploader("  Upload an academic image", type=["jpg", "png", "jpeg"])
    mode = summarization_mode_selector()
    return image, mode
