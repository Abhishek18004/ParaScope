"""
This is the core logic to generate summaries using the Gemini API. It takes cleaned input, selects the 
right prompt (summary, glossary, or full), and returns cleaned output text.
"""

import os
import sys
import re

# Dynamically add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import google.generativeai as genai
from config import GEMINI_API_KEY
from app.prompts import SUMMARY_ONLY, SUMMARY_GLOSSARY, GLOSSARY, FULL_ANALYSIS

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)

def call_gemini(prompt: str) -> dict:
    """
    Calls Gemini Pro model with the given prompt.
    Returns a dictionary with success flag and output text or error.
    """
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return {
            "success": True,
            "output": response.text
        }
    except Exception as e:
        print(f"[Gemini API Error] {e}")
        return {
            "success": False,
            "output": f"[Gemini Error]: {str(e)}"
        }

def clean_response(text: str) -> str:
    """
    Cleans Gemini's output by removing assistant-like preambles.
    """
    try:
        text = re.sub(r"^(Sure!|Of course!|Here's|Let me explain.*?:?)", '', text.strip(), flags=re.IGNORECASE)
        return text.strip()
    except Exception as e:
        print(f"[Clean Error] Failed to clean response: {e}")
        return text.strip()

def summarize_text(cleaned_text: str, mode: str = "summary_glossary") -> dict:
    """
    Uses Gemini to summarize the academic text based on selected mode:
    - 'summary'
    - 'summary_glossary'
    - 'glossary'
    - 'full'
    Returns a consistent response dict with success flag and output.
    """
    try:
        prompt_map = {
            "summary": SUMMARY_ONLY,
            "summary_glossary": SUMMARY_GLOSSARY,
            "glossary": GLOSSARY,
            "full": FULL_ANALYSIS
        }

        if not cleaned_text or len(cleaned_text.strip()) < 10:
            return {
                "success": False,
                "output": "[Input Error]: Input text is too short or empty."
            }

        prompt_template = prompt_map.get(mode, SUMMARY_GLOSSARY)
        prompt = prompt_template.format(inputData=cleaned_text)

        gemini_result = call_gemini(prompt)
        if gemini_result["success"]:
            return {
                "success": True,
                "output": clean_response(gemini_result["output"])
            }
        else:
            return gemini_result

    except Exception as e:
        print(f"[Summarization Error] {e}")
        return {
            "success": False,
            "output": f"[Summarization Error]: {str(e)}"
        }
