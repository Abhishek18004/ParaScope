"""
This file validates user input to ensure it's long enough and contains technical terms, acting as a 
quality filter for academic relevance. It also preprocesses the input by cleaning and normalizing it 
via clean_text().

"""

import os
import sys
import re

# Dynamically add the root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.cleaners import clean_text


# change size to 150
def validate_text(text: str, min_words: int = 30) -> dict:
    """Validates text for minimum length and presence of technical terms."""
    word_count = len(text.split())
    if word_count < min_words:
        return {"valid": False, "error": f"Text too short ({word_count} words)"}

#figure out this thingy, figure out s's
    if not re.search(r'\b(et al|p-value|hypothesis|algorithm|dataset|model)\b', text, re.IGNORECASE):
        return {"valid": False, "error": "Text does not appear to be scientific/technical"}

    return {"valid": True}

#figure out abt "s" how it understands
def preprocess_text(text: str) -> str:
    """
    Applies basic cleaning, removes LaTeX, citation brackets, lowercases text.
    """
    cleaned = clean_text(text)
    return cleaned