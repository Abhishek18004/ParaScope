# [Glossary generation failed]

"""
Breaks large text sections into ~300-word chunks, sends them to the summarizer model, and merges 
the summaries. Applies per-section and full-paper summarization and generates a glossary for the 
complete document.
"""

import os
import sys
import re

# Add project root to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from app.summarizer import summarize_text
from utils.cleaners import clean_text

def smart_chunk_text(text: str, max_words: int = 300) -> list:
    """
    Breaks text into semantically meaningful chunks (~max_words each),
    preserving paragraph or sentence boundaries.
    """
    paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
    
    chunks = []
    current_chunk = []

    def chunk_word_count(chunk_list):
        return sum(len(p.split()) for p in chunk_list)

    for para in paragraphs:
        current_chunk.append(para)
        if chunk_word_count(current_chunk) >= max_words:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []

    if current_chunk:
        chunks.append('\n'.join(current_chunk))

    return chunks

def summarize_section(section_title: str, section_text: str, mode: str = "summary") -> str:
    """
    Summarizes a single section of the paper using smart chunking.
    Returns the full section summary in markdown format.
    """
    if not section_text or len(section_text.strip()) < 30:
        return f"### {section_title}\n[Skipped]: Section content too short or empty."

    try:
        cleaned = clean_text(section_text)
        chunks = smart_chunk_text(cleaned)

        summaries = []
        for i, chunk in enumerate(chunks):
            try:
                result = summarize_text(chunk, mode=mode)
                if result["success"]:
                    summaries.append(result["output"])
                else:
                    print(f"[Summary Error] Chunk {i+1} of '{section_title}' failed.")
                    summaries.append("[Error in summarization]")
            except Exception as e:
                print(f"[Chunk Error] Failed to summarize chunk {i+1} of '{section_title}': {e}")
                summaries.append(f"[Error]: Failed to summarize chunk {i+1} – {str(e)}")

        full_summary = "\n".join(summaries)
        return f"### {section_title}\n{full_summary.strip()}"

    except Exception as e:
        print(f"[Section Error] Failed to summarize section '{section_title}': {e}")
        return f"### {section_title}\n[Error]: Failed to summarize section – {str(e)}"

def summarize_full_paper(section_dict: dict, mode: str = "summary") -> str:
    """
    Summarizes all sections of the paper using the selected mode.
    Returns a full paper summary.
    """
    all_summaries = []
    try:
        for title, content in section_dict.items():
            summary = summarize_section(title, content, mode=mode)
            all_summaries.append(summary)

        return "\n\n".join(all_summaries)

    except Exception as e:
        print(f"[Paper Error] Failed to summarize full paper: {e}")
        return "[Error]: Failed to generate full paper summary."

def extract_global_glossary(full_text: str) -> str:
    """
    Generates a glossary from the full academic text.
    Returns glossary or error message string.
    """
    try:
        cleaned = clean_text(full_text)
        result = summarize_text(cleaned, mode="glossary")
        return result["output"] if result["success"] else "[Glossary generation failed]"
    except Exception as e:
        print(f"[Glossary Error] Failed to extract glossary: {e}")
        return f"[Error]: Glossary generation failed – {str(e)}"

# Example usage
if __name__ == "__main__":
    from input.pdf_extractor import extract_text_from_pdf, split_into_sections

    pdf_path = r"C:\Users\HP\Documents\Projects\ParaScope\academic_summarizer\data\sample_paper_1.pdf"

    result = extract_text_from_pdf(pdf_path)
    if not result["success"]:
        print(result["output"])
    else:
        sections = split_into_sections(result["output"])
        print("==== Final Layered Summary ====\n")
        full_summary = summarize_full_paper(sections, mode="summary_glossary")
        print(full_summary[:1500])  # Preview

        print("\n==== Global Glossary ====\n")
        glossary = extract_global_glossary(result["output"])
        print(glossary[:1000])  # Preview
