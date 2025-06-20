"""
Loads an academic/scientific image, pre-processes it (grayscale, contrast enhancement, border trim), and 
uses Gemini Vision to extract the text. Cleans common OCR errors like non-ASCII characters, symbol 
misreads, and spacing issues to ensure clean input for summarization.
"""

# inputs/image_ocr.py
import os
import sys
import re

# Dynamically add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

import google.generativeai as genai
from PIL import Image, ImageOps
from config import GEMINI_API_KEY

# Configure Gemini Vision
genai.configure(api_key=GEMINI_API_KEY)

def preprocess_image(image_path: str) -> dict:
    """
    Preprocess image: convert to grayscale, remove border, enhance contrast.
    Returns a dict with success flag and result or error message.
    """
    try:
        img = Image.open(image_path)
        img = ImageOps.grayscale(img)
        img = ImageOps.autocontrast(img)
        img = ImageOps.expand(img, border=-10)  # Try to trim 10px border
        return {"success": True, "image": img}
    except Exception as e:
        print(f"[Image Error] Failed to preprocess image: {e}")
        return {"success": False, "output": f"[OCR Error]: Failed to load or preprocess image – {str(e)}"}

def extract_text_from_image(image: Image.Image) -> dict:
    """
    Use Gemini Vision to extract academic/scientific text from image.
    Returns dict with success and extracted text or error message.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content([
            "Extract academic text from this image for summarization:",
            image
        ])
        return {"success": True, "output": response.text}
    except Exception as e:
        print(f"[OCR Error] Gemini OCR failed: {e}")
        return {"success": False, "output": f"[OCR Error]: {str(e)}"}

def clean_ocr_text(text: str) -> str:
    """
    Cleans up common OCR issues: random characters, math symbol misreads.
    Returns a cleaned string.
    """
    try:
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII
        text = re.sub(r'\s+', ' ', text)
        text = text.replace('¬', '-')  # Common OCR error for minus sign
        return text.strip()
    except Exception as e:
        print(f"[Clean Error] Failed to clean OCR text: {e}")
        return "[OCR Error]: Failed to clean extracted text"
