"""
Contains predefined prompt templates for Gemini to generate summaries, glossaries, and comprehension 
questions. These templates are dynamically filled with user input text before being sent to the model.
"""

SUMMARY_ONLY = """
You are an academic assistant. Simplify the following scientific text. Provide:

1. A summary in 200-250 words.

Text:
{inputData}

Respond with only the simplified summary as heading:
### Summary
"""

SUMMARY_GLOSSARY = """
You are an academic assistant. Simplify the following scientific text. Provide:

1. A concise summary in 200-250 words.
2. A glossary of all the technical terms, order from simple to complex based on their conceptual difficulty and their relational or usage hierarchy.

Text:
{inputData}

Respond with these two headings only:
### Summary
### Glossary of terms (term: definition)
"""

GLOSSARY = """
You are an academic assistant. Simplify the following scientific text. Provide:

1. A glossary of all the technical terms, order from simple to complex based on their conceptual difficulty and their relational or usage hierarchy.

Text:
{inputData}

Respond with this heading only:
### Glossary of terms (term: definition)
"""

FULL_ANALYSIS = """
You are an academic assistant. Simplify the following scientific text. Provide:

1. A concise summary in 200-250 words.
2. A glossary of all the technical terms, order from simple to complex based on their conceptual difficulty and their relational or usage hierarchy.
3. Create 2 to 3 comprehension questions with answers that test deeper understanding, focusing on hidden connections and application-based insights.

Text:
{inputData}

Respond with these three headings only:
### Summary
### Glossary
### Questions
"""

OCR_SUMMARIZE_PROMPT = """
You are an academic assistant. Given the messy academic notes or scanned OCR text below, reconstruct a clean academic summary.

Text:
{inputData}

Instructions:
- Fix structure if missing.
- Ignore noise or irrelevant characters.
- Provide a clear academic summary.
- Include any key concepts or terms.
- If math symbols or Greek letters are mentioned, explain briefly.
"""