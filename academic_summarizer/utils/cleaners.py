"""
This file removes LaTeX expressions, citations, and extra whitespace from text input, and converts it to 
lowercase. It helps prepare cleaner input for processing or feeding into a model.
"""

import re

def clean_text(text: str) -> str:
    #Cleans input text by removing LaTeX, citations, and normalizing whitespace.
    text = text.encode('utf-8', 'ignore').decode()  # remove non-UTF-8
    text = re.sub(r'\[(\d+|[A-Za-z]+)\]', '', text)  # remove citations [1], [Smith]
    text = re.sub(r'\$.*?\$', '', text)  # remove inline LaTeX like $E=mc^2$
    text = re.sub(r'\\[a-zA-Z]+', '', text)  # remove LaTeX commands like \cite
    text = re.sub(r'\s+', ' ', text)
    return text.strip().lower()
