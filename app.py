import streamlit as st

# Import flat functions
from src.config import (
    TRANSLATION_DIRECTIONS, MAX_FILE_SIZE_MB,
    ERROR_MESSAGES, SUCCESS_MESSAGES
)
from src.pdf_reader import (
    validate_pdf, get_pdf_info, has_extractable_text,
    extract_text_blocks
)
from src.translator import translate_text_blocks, translate_text
from src.pdf_writer import (
    create_translated_pdf, create_simple_translated_pdf
)
from src.postprocessing import preprocess_text

def render_sidebar():
    with st.sidebar:
        st.header("ℹ️ About")
        st.write("✅ Latest version deployed successfully!")
        st.markdown("""
        This app translates PDF content between Hindi and English.
        - ✅ Smart text filtering
        - ✅ Layout preservation
        - ✅ Free Google Translate via Deep Translator
        - ✅ Multi-page PDFs Support
        """)

        st.header("🧠 Test Filtering")
        demo_text = st.text_input("Try intelligent filtering:", value="Welcome to the Sample Application! This user manual will guide you through the installation, setup, and usage of the application. Follow the steps below to get started quickly and effectively.")
        if demo_text:
            segments = preprocess_text(demo_text)
            for word, should_tx in segments:
                color = "🟢" if should_tx else "🔴"
                st.write(f"{color} `{word}`")
            translated = translate_text(demo_text, 'en', 'hi')
            st.markdown(f"**Translated Result:** {translated}")


# Render MAIN FIle
def render_header():
    st.title("📄 PDF Translator - Amalgo Task 2")
    st.markdown("### Translate PDFs between Hindi ↔ English")


def render_file_upload():
    st.header("1️⃣ Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])
    if uploaded_file:
        if len(uploaded_file.getvalue()) > MAX_FILE_SIZE_MB * 1024 * 1024:
            st.error(ERROR_MESSAGES["file_too_large"])
            return None

        if not validate_pdf(uploaded_file.getvalue()):
            st.error(ERROR_MESSAGES["invalid_format"])
            return None

        info = get_pdf_info(uploaded_file.getvalue())
        col1, col2, col3 = st.columns(3)
        col1.metric("Pages", info["page_count"])
        col2.metric("Size", f"{info['size_bytes'] // 1024} KB")
        if info["page_width"] and info["page_height"]:
            col3.metric("Dimensions", f"{int(info['page_width'])}×{int(info['page_height'])}")

        if not has_extractable_text(uploaded_file.getvalue()):
            st.warning(ERROR_MESSAGES["empty_pdf"])
            return None

        st.success("✅ PDF uploaded successfully!")
        return uploaded_file
    return None

def render_translation_direction():
    st.header("2️⃣ Select Translation Direction")
    direction = st.selectbox("Direction:", list(TRANSLATION_DIRECTIONS.keys()))
    source_lang, target_lang = TRANSLATION_DIRECTIONS[direction]
    col1, col2 = st.columns(2)
    col1.info(f"From: {direction.split(' to ')[0]}")
    col2.info(f"To: {direction.split(' to ')[1]}")
    return source_lang, target_lang

def run_translation(uploaded_file, source_lang, target_lang):
    st.header("3️⃣ Translate PDF")
    if st.button("🚀 Start Translation"):
        progress = st.progress(0.0)
        status = st.empty()

        file_bytes = uploaded_file.getvalue()
        status.text("📖 Extracting text...")
        progress.progress(0.1)
        blocks = extract_text_blocks(file_bytes)

        if not blocks:
            st.error("No text blocks found. May be image-only.")
            return None

        texts = [b['text'] for b in blocks]

        def callback(p, msg):  # Progress updater
            progress.progress(0.3 + p * 0.5)
            status.text(f"🔄 {msg}")

        status.text("🔄 Translating...")
        translated = translate_text_blocks(texts, source_lang, target_lang, callback)

        progress.progress(0.85)
        status.text("📄 Generating PDF...")
        pdf_bytes = create_translated_pdf(file_bytes, blocks, translated)

        if not pdf_bytes:
            status.text("📄 Using fallback layout...")
            combined_text = "\n".join(translated)
            pdf_bytes = create_simple_translated_pdf(combined_text, file_bytes)

        progress.progress(1.0)
        status.text("✅ Translation completed!")

        st.session_state.translation_complete = True
        st.session_state.translated_pdf_bytes = pdf_bytes
        st.session_state.original_filename = uploaded_file.name

        st.success(SUCCESS_MESSAGES["translation_complete"])
        col1, col2, col3 = st.columns(3)
        col1.metric("Blocks", len(blocks))
        col2.metric("Characters", sum(len(t) for t in texts))
        col3.metric("Size", f"{len(pdf_bytes) // 1024} KB")

def render_download_section():
    if st.session_state.get("translation_complete"):
        st.header("4️⃣ Download Translated PDF")
        original_name = st.session_state.get("original_filename", "document")
        base = original_name.rsplit(".", 1)[0]
        translated_bytes = st.session_state.get("translated_pdf_bytes")

        st.download_button(
            label="📥 Download",
            data=translated_bytes,
            file_name=f"{base}_translated.pdf",
            mime="application/pdf"
        )

        if st.button("🔄 Translate Another"):
            st.session_state.translation_complete = False
            st.session_state.translated_pdf_bytes = None
            st.session_state.original_filename = None
            st.rerun()

def main():
    st.set_page_config(page_title="PDF Translator", page_icon="📄", layout="wide")
    render_sidebar()
    render_header()

    uploaded_file = render_file_upload()
    if uploaded_file:
        source, target = render_translation_direction()
        run_translation(uploaded_file, source, target)

    render_download_section()

if __name__ == "__main__":
    main()
