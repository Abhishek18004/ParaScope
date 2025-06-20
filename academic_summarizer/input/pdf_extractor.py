"""
Extracts clean, readable text from each page of a PDF by removing headers, footers, and page numbers.
Splits the full text into academic sections (like Introduction, Methods) based on structured headings 
using regex.
"""

import pdfplumber
import re

def extract_text_from_pdf(pdf_path: str) -> dict:
    try:
        full_text = []

        with pdfplumber.open(pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                try:
                    text = page.extract_text()
                    if not text:
                        continue

                    lines = text.split('\n')
                    filtered_lines = []

                    for line in lines:
                        # Remove page numbers
                        if re.match(r'^\s*\d+\s*$', line.strip()):
                            continue
                        # Remove short repeated headers/footers
                        if len(line.strip()) < 5:
                            continue
                        filtered_lines.append(line)

                    cleaned_page = '\n'.join(filtered_lines)
                    full_text.append(cleaned_page)

                except Exception as pe:
                    print(f"[PDF Error] Failed to read page {page_num + 1}: {pe}")
                    return {
                        "success": False,
                        "output": f"[PDF Error]: Failed to extract text from page {page_num + 1}"
                    }

        if not full_text:
            return {
                "success": False,
                "output": "[PDF Error]: No text found in PDF"
            }

        combined_text = '\n'.join(full_text).strip()
        return {
            "success": True,
            "output": combined_text
        }

    except Exception as e:
        print(f"[PDF Error] Could not open or process file: {e}")
        return {
            "success": False,
            "output": f"[PDF Error]: Could not open or process PDF file – {e}"
        }


def split_into_sections(text: str) -> dict:
    """
    Splits PDF text into logical sections using common academic headers.
    Returns: { section_name: section_content }
    """
    try:
        sections = {}
        current_section = "Preface"
        buffer = []

        for line in text.split('\n'):
            # Match headers like: 1. Introduction, 2. Methods, etc.
            match = re.match(r'^\s*(\d+(\.\d+)?)[\.\)]?\s+([A-Z][a-zA-Z ]+)$', line.strip())
            if match:
                if buffer:
                    sections[current_section] = '\n'.join(buffer).strip()
                    buffer = []
                current_section = match.group(3).strip()
            buffer.append(line)

        # Final section
        if buffer:
            sections[current_section] = '\n'.join(buffer).strip()

        if not sections:
            print("[PDF Warning] No sections found using regex.")
        return sections

    except Exception as e:
        print(f"[PDF Error] Failed to split into sections: {e}")
        return {
            "Preface": f"[PDF Error]: Failed to split sections – {str(e)}"
        }

# 🔍 Example usage
if __name__ == "__main__":
    pdf_path = r"C:\Users\HP\Documents\Projects\ParaScope\academic_summarizer\data\sample_paper_1.pdf"

    result = extract_text_from_pdf(pdf_path)

    if not result["success"]:
        print(result["output"])
    else:
        sections = split_into_sections(result["output"])
        for sec, content in sections.items():
            print(f"\n--- {sec} ---\n{content[:500]}...\n")
