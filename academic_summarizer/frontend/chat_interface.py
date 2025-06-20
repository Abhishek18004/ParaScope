# frontend/chat_interface.py

import streamlit as st
from frontend.display import text_input_ui, pdf_input_ui, image_input_ui
from input.text_input import preprocess_text, validate_text
from input.pdf_extractor import extract_text_from_pdf, split_into_sections
from input.image_ocr import preprocess_image, extract_text_from_image, clean_ocr_text
from input.chunk_and_summarize import summarize_full_paper
from app.ocr_summarizer import summarize_ocr_text
from app.summarizer import summarize_text

def academic_chatbot():
    tab = st.radio("Choose Input Type", ["📝 Text", "📄 PDF", "🖼 Image"], horizontal=True)

    if tab == "📝 Text":
        text, mode = text_input_ui()
        if st.button("Submit"):
            if not text.strip():
                st.error("⚠️ Please enter academic text.")
                return
            result = validate_text(text)
            if not result["valid"]:
                st.warning(result["error"])
                return
            with st.spinner("🔍 Analyzing academic text..."):
                cleaned = preprocess_text(text)
                response = summarize_text(cleaned, mode=convert_mode(mode))
                if response["success"]:
                    display_output(response["output"], mode="text")
                else:
                    st.error(response["output"])

    elif tab == "📄 PDF":
        file, mode = pdf_input_ui()
        if st.button("Submit"):
            if not file:
                st.error("⚠️ Please upload a PDF file.")
                return
            with st.spinner("🔍 Extracting and analyzing PDF..."):
                pdf_result = extract_text_from_pdf(file)
                if not pdf_result["success"]:
                    st.error(pdf_result["output"])
                    return
                sections = split_into_sections(pdf_result["output"])
                result = summarize_full_paper(sections, mode=convert_mode(mode))
                display_output(result, mode="pdf")

    elif tab == "🖼 Image":
        image, mode = image_input_ui()
        if st.button("Submit"):
            if not image:
                st.error("⚠️ Please upload an image file.")
                return
            with st.spinner("🔍 Processing image and analyzing content..."):
                img_result = preprocess_image(image)
                if not img_result["success"]:
                    st.error(img_result["output"])
                    return
                text_result = extract_text_from_image(img_result["image"])
                if not text_result["success"]:
                    st.error(text_result["output"])
                    return
                cleaned = clean_ocr_text(text_result["output"])
                response = summarize_ocr_text(cleaned, mode=convert_mode(mode))
                if response["success"]:
                    if response["low_confidence"]:
                        st.warning("⚠️ Low-confidence OCR detected. Text may be noisy.")
                    display_output(response["summary"], mode="text")
                else:
                    st.error(response["output"])

def display_output(output_text: str, mode="text"):
    """
    Renders summarizer output.

    - PDF mode: Groups by section, filters out empty sections, supports global glossary/QnA.
    - Text/Image: Flat expanders for each section block.
    """
    if mode == "pdf":
        section_blocks = output_text.strip().split("### ")
        section_map = {}
        global_parts = {}

        current_section = None

        for block in section_blocks:
            if not block.strip():
                continue

            lines = block.strip().split("\n")
            heading = lines[0].strip()
            content = "\n".join(lines[1:]).strip()

            if heading.lower() not in ["summary", "glossary", "questions"]:
                current_section = heading
                section_map[current_section] = {}
            elif current_section:
                if content.strip():
                    section_map[current_section][heading.capitalize()] = content
            else:
                if content.strip():
                    global_parts[heading.capitalize()] = content

        # Show only sections that contain at least one of Summary, Glossary, Questions
        for section_title, sub_parts in section_map.items():
            if any(key in sub_parts for key in ["Summary", "Glossary", "Questions"]):
                st.subheader(f"📘 {section_title}")

                if "Summary" in sub_parts:
                    with st.expander("📄 Summary"):
                        st.markdown(sub_parts["Summary"])

                if "Glossary" in sub_parts:
                    with st.expander("📘 Glossary"):
                        st.markdown(sub_parts["Glossary"])

                if "Questions" in sub_parts:
                    with st.expander("❓ Questions"):
                        st.markdown(sub_parts["Questions"])

                st.markdown("")  # space between sections

        # Show global parts (not tied to any section)
        if global_parts:
            st.subheader("📚 Global Analysis")
            if "Summary" in global_parts:
                with st.expander("📄 Summary"):
                    st.markdown(global_parts["Summary"])
            if "Glossary" in global_parts:
                with st.expander("📘 Glossary"):
                    st.markdown(global_parts["Glossary"])
            if "Questions" in global_parts:
                with st.expander("❓ Questions"):
                    st.markdown(global_parts["Questions"])

    else:
        # Flat expanders for text/image modes
        for section in output_text.strip().split("###"):
            if section.strip():
                title, *body = section.strip().split("\n", 1)
                if body and body[0].strip():
                    with st.expander(f"📌 {title.strip()}"):
                        st.markdown(body[0])


def convert_mode(mode_label: str) -> str:
    return {
        "Summary": "summary",
        "Summary + Glossary": "summary_glossary",
        "Only Glossary": "glossary",
        "Full (Summary + Glossary + Analysis Q/A)": "full"
    }.get(mode_label, "summary")
