# frontend/layout.py
import streamlit as st

def custom_styling():
    st.markdown("""
        <style>
        /* Hide default Streamlit header */
        header { visibility: hidden; }

        /* Background & Global Text Colors */
        body, .main, .block-container, .stApp {
            background-color: #1b1c1f !important;
            color: #aeb0b3 !important;
        }

        /* Heading (H1-H3) Styling */
        h1, h2, h3 {
            color: #f5f5f5 !important;
        }

                
        /* Subheadings and Captions */
        .st-emotion-cache-1v0mbdj,
        .stCaption,
        .stMarkdown small {
            color: #c9c9ce !important;
        }

        /* Buttons */
        .stButton>button {
            background-color: #b22234;
            color: white;
            font-size: 16px;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            font-weight: bold;
            border: none;
        }
        .stButton>button:hover {
            background-color: #600b16;
            color: white;
        }

        /* Radio Buttons */
        .stRadio > div {
            color: #ff4b4b !important;
            font-weight: bold;
        }

        /* File Uploader + Textarea (Input Boxes) */
        textarea, .stFileUploader {
            background-color: #262730 !important;
            color: #f5f5f5 !important;
            border-radius: 10px;
            padding: 0.5em;
            font-size: 15px;
        }

        /* Markdown Output Box */
        .markdown-text-container {
            background-color: #1b1c1f !important;
            color: #aeb0b3 !important;
        }

        /* Expander Title */
        .st-expander > summary {
            background-color: #262730 !important;
            color: #ffc857 !important;
            font-weight: bold;
            border-radius: 8px;
            border: 2px solid #ffc857 !important; /* Outline color */
            padding: 0.6em;
            transition: background-color 0.3s, border-color 0.3s;
        }

        /* Expander Hover Effect */
        .st-expander > summary:hover {
            background-color: #32333e !important;
            border-color: #ffdc73 !important;
            cursor: pointer;
        }

        /* Code blocks (optional improvement for markdown code) */
        pre, code {
            background-color: #262730 !important;
            color: #ffc857 !important;
            border-radius: 6px;
        }
                
        /* Horizontal rule styling */
        hr {
            border-color: #1a0d0f !important;  /* Same as background to make it invisible */
        }
        </style>
    """, unsafe_allow_html=True)

def show_header():
    st.markdown(
        """
        <div style='
            background-color: #600b16;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
        '>
            <h1 style='color: #ffffff; margin-bottom: 0.5rem;'>ParaScope</h1>
            <h4 style='color: #ffc9c9; margin-top: 0;'>Academic Paper Summarizer & Analyzer</h4>
            <p style='color: #ff9e9e; font-size: 1.1rem;'>Use text, PDFs, or images to summarize and comprehend academic papers.</p>
        </div>
        <br/>
        <hr/>
        """,
        unsafe_allow_html=True
    )

