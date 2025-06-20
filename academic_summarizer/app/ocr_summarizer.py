"""
Performs quality checks on OCR-extracted text to detect low-information content before summarization.
Cleans the text and runs it through a summarizer using different modes (summary, glossary, etc.), 
returning the result with a confidence flag.
"""

# app/ocr_summarizer.py

import os
import sys
import re

# Dynamically add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.prompts import OCR_SUMMARIZE_PROMPT
from app.summarizer import summarize_text
from utils.cleaners import clean_text

def is_text_quality_low(text: str, min_words: int = 50) -> bool:
    """
    Checks whether the text is likely to produce a low-confidence summary.
    """
    word_count = len(text.split())
    if word_count < min_words:
        return True
    if not re.search(r'\b(method|model|algorithm|data|accuracy|loss|experiment)\b', text, re.IGNORECASE):
        return True
    return False

def summarize_ocr_text(ocr_text: str, mode="summary", model="gemini") -> dict:
    """
    Cleans and summarizes OCR-extracted academic text.
    Accepts a mode: summary, glossary, summary_glossary, full.
    Returns a dictionary: { success, summary, low_confidence } or error message.
    """
    result = {
        "success": False,
        "summary": "",
        "low_confidence": False
    }

    try:
        if not ocr_text or len(ocr_text.strip()) < 20:
            return {
                "success": False,
                "output": "[OCR Error]: Extracted text is empty or too short."
            }

        cleaned_text = clean_text(ocr_text)
        result["low_confidence"] = is_text_quality_low(cleaned_text)

        summarize_result = summarize_text(cleaned_text, mode=mode)

        if summarize_result.get("success"):
            result["success"] = True
            result["summary"] = summarize_result["output"]
        else:
            print("[OCR Summarization Error]: Gemini summarization failed.")
            result["summary"] = "[Summarization failed]"

        return result

    except Exception as e:
        print(f"[OCR Summary Exception]: {e}")
        return {
            "success": False,
            "output": f"[OCR Error]: Failed to summarize OCR text – {str(e)}"
        }
