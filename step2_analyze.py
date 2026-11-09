
import os
import re
import json
import hashlib
from datetime import datetime

import fitz
import streamlit as st
from groq import Groq
from dotenv import load_dotenv


# =====================================================
# SNAKES AI — DOCUMENT INTELLIGENCE WORKSPACE
# =====================================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL = "openai/gpt-oss-20b"

DATA_FILE = "snakes_history.json"
DOCUMENT_FOLDER = "uploaded_documents"

os.makedirs(DOCUMENT_FOLDER, exist_ok=True)

st.set_page_config(
    page_title="SNAKES AI",
    page_icon="🐍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# HTML RENDERING HELPER
# =====================================================

def render_html(content):
    # Remove leading indentation so Markdown never treats HTML as a code block.
    clean_content = "\n".join(line.lstrip() for line in content.splitlines())
    st.markdown(clean_content, unsafe_allow_html=True)


# =====================================================
# CUSTOM CSS
# =====================================================

CSS = """
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --black: #111111;
    --white: #ffffff;
    --grey: #777777;
    --light: #f3f3f3;
    --border: #e5e5e5;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #f3f3f3;
    color: #111111;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    max-width: 1050px;
    padding-top: 25px;
    padding-bottom: 50px;
}

/* SIDEBAR */

section[data-testid="stSidebar"] {
    background: #111111 !important;
    border-right: 1px solid #292929;
}

section[data-testid="stSidebar"] * {
    color: #ffffff;
}

section[data-testid="stSidebar"] .stButton button {
    background: #222222 !important;
    color: #ffffff !important;
    border: 1px solid #363636 !important;
    border-radius: 10px !important;
    text-align: left;
    min-height: 42px;
}

section[data-testid="stSidebar"] .stButton button:hover {
    background: #383838 !important;
}

/* SIDEBAR HISTORY */

.history-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 23px;
    font-weight: 800;
    color: #ffffff;
    margin-bottom: 5px;
}

.history-subtitle {
    color: #999999;
    font-size: 12px;
    margin-bottom: 25px;
}

.history-label {
    color: #999999;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-top: 25px;
    margin-bottom: 10px;
}

/* MAIN HEADER */

.main-header {
    background: #111111;
    border-radius: 20px;
    padding: 42px 20px;
    text-align: center;
    margin-bottom: 30px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.08);
}

.main-brand {
    color: #aaaaaa;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 4px;
    margin-bottom: 15px;
}

.main-title {
    color: #ffffff;
    font-family: 'Manrope', sans-serif;
    font-size: clamp(30px, 5vw, 43px);
    font-weight: 800;
    letter-spacing: -1.5px;
}

.main-description {
    color: #bbbbbb;
    font-size: 14px;
    margin-top: 12px;
}

/* SNAKE ANIMATION */

.snake {
    display: inline-block;
    font-size: 43px;
    animation: snakeMove 2.5s ease-in-out infinite;
}

@keyframes snakeMove {
    0%, 100% {
        transform: translateY(0px) rotate(-8deg);
    }

    50% {
        transform: translateY(-10px) rotate(8deg);
    }
}

/* MAIN CARDS */

.main-card {
    background: #ffffff;
    border: 1px solid #e5e5e5;
    border-radius: 17px;
    padding: 23px;
    box-shadow: 0 5px 22px rgba(0,0,0,0.025);
    margin-bottom: 18px;
}

.section-heading {
    font-family: 'Manrope', sans-serif;
    font-size: 20px;
    font-weight: 800;
    color: #111111;
    margin-bottom: 8px;
}

.section-description {
    font-size: 13px;
    color: #777777;
    line-height: 1.7;
}

/* UPLOADER */

.stFileUploader section {
    background: #ffffff !important;
    border: 1.5px dashed #aaaaaa !important;
    border-radius: 13px !important;
}

.stFileUploader section * {
    color: #222222 !important;
}

/* BUTTONS */

.stButton button,
.stFormSubmitButton button,
.stDownloadButton button {
    background: #111111 !important;
    color: #ffffff !important;
    border: 1px solid #111111 !important;
    border-radius: 10px !important;
    min-height: 43px;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

.stButton button:hover,
.stFormSubmitButton button:hover,
.stDownloadButton button:hover {
    background: #333333 !important;
    border-color: #333333 !important;
    transform: translateY(-1px);
}

/* SEARCH INPUT */

.stTextInput input {
    background: #ffffff !important;
    color: #111111 !important;
    border: 1.5px solid #222222 !important;
    border-radius: 11px !important;
    min-height: 45px;
}

.stTextInput input:focus {
    border-color: #000000 !important;
    box-shadow: 0 0 0 1px #111111 !important;
}

/* ANSWER CARD */

.answer-card {
    background: #ffffff;
    border: 1px solid #e4e4e4;
    border-radius: 15px;
    padding: 22px;
    margin-top: 15px;
}

div[data-testid="stAlert"] {
    border-radius: 11px;
}

/* HISTORY EXPANDER */

section[data-testid="stSidebar"] div[data-testid="stExpander"] {
    background: #202020;
    border: 1px solid #363636;
    border-radius: 10px;
}

section[data-testid="stSidebar"] div[data-testid="stExpander"] * {
    color: #eeeeee;
}

/* FOOTER */

.footer-text {
    text-align: center;
    color: #999999;
    font-size: 11px;
    margin-top: 50px;
}

/* MOBILE */

@media (max-width: 768px) {

    .block-container {
        padding: 15px 13px 35px;
    }

    .main-header {
        padding: 32px 15px;
    }

    .main-title {
        font-size: 29px;
    }

    .main-card {
        padding: 17px;
    }

}

</style>
"""

render_html(CSS)


# =====================================================
# SESSION STATE
# =====================================================

def load_history():

    if not os.path.exists(DATA_FILE):
        return {}

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, dict) else {}

    except (json.JSONDecodeError, OSError):
        return {}


if "documents" not in st.session_state:
    st.session_state.documents = load_history()

if "active_document" not in st.session_state:
    st.session_state.active_document = None


# =====================================================
# SAVE HISTORY
# =====================================================

def save_history():

    temporary_file = DATA_FILE + ".tmp"

    with open(temporary_file, "w", encoding="utf-8") as file:

        json.dump(
            st.session_state.documents,
            file,
            ensure_ascii=False,
            indent=2
        )

    os.replace(temporary_file, DATA_FILE)


# =====================================================
# PDF EXTRACTION
# =====================================================

def extract_text_from_pdf(file_bytes):

    doc = fitz.open(
        stream=file_bytes,
        filetype="pdf"
    )

    try:
        pages = [
            page.get_text("text")
            for page in doc
        ]

    finally:
        doc.close()

    raw_text = "\n".join(pages)

    lines = [
        line.strip()
        for line in raw_text.split("\n")
        if line.strip()
    ]

    return "\n".join(lines)


# =====================================================
# TEXT CHUNKING
# =====================================================

def create_chunks(text, chunk_size=250, overlap=40):

    words = text.split()
    chunks = []

    start = 0

    while start < len(words):

        end = start + chunk_size

        chunk = " ".join(words[start:end])

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# =====================================================
# DOCUMENT RETRIEVAL
# =====================================================

def retrieve_chunks(question, chunks, top_k=4):

    stop_words = {
        "what", "where", "when", "which", "who",
        "why", "how", "does", "did", "the",
        "and", "for", "are", "was", "were",
        "is", "in", "on", "of", "to", "a",
        "an", "this", "that", "my", "me",
        "can", "could", "please", "tell",
        "about", "from", "with", "have",
        "has", "do", "i", "it"
    }

    question_words = set(
        re.findall(
            r'\b[a-zA-Z0-9]+\b',
            question.lower()
        )
    )

    question_words -= stop_words

    if not question_words:
        return []

    results = []

    for index, chunk in enumerate(chunks):

        chunk_words = set(
            re.findall(
                r'\b[a-zA-Z0-9]+\b',
                chunk.lower()
            )
        )

        matches = question_words.intersection(chunk_words)

        score = len(matches)

        if score > 0:
            results.append((score, index, chunk))

    results.sort(
        key=lambda item: item[0],
        reverse=True
    )

    return [
        item[2]
        for item in results[:top_k]
    ]


# =====================================================
# GROQ CLIENT
# =====================================================

def get_client():

    if not API_KEY:
        raise ValueError("API configuration unavailable.")

    return Groq(api_key=API_KEY)


# =====================================================
# DOCUMENT ANALYSIS
# =====================================================

def analyze_document(document_text):

    client = get_client()

    prompt = f"""
You are SNAKES AI, a professional document analyzer.

Analyze the uploaded document.

Use these sections:

## 1. Document Overview
Explain what the document contains.

## 2. Important Information
Identify the important information.

## 3. Key Points
Summarize the main points.

## 4. Important Details
Identify useful details from the document.

## 5. Final Summary
Give a clear and helpful conclusion.

RULES:
- Use only the uploaded document.
- Do not invent information.
- Be professional and clear.
- Use organized Markdown.
- Do not reproduce the complete document.

DOCUMENT CONTENT:

{document_text}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a professional document analyzer."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content


# =====================================================
# ASK DOCUMENT QUESTION
# =====================================================

def ask_document(question, chunks):

    relevant_chunks = retrieve_chunks(
        question,
        chunks,
        top_k=4
    )

    if not relevant_chunks:

        return (
            "I could not find relevant information "
            "about this question in your uploaded document."
        )

    context = "\n\n".join(relevant_chunks)

    client = get_client()

    prompt = f"""
You are SNAKES AI, a document-based assistant.

Answer the question using ONLY the supplied document sections.

RULES:

1. Only use supplied document information.
2. Never use outside information.
3. Never invent facts.
4. If the answer is missing, clearly say so.
5. Give a direct and helpful answer.
6. Never reproduce the complete document.
7. Do not display retrieved chunks.

DOCUMENT INFORMATION:

{context}

USER QUESTION:

{question}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer strictly using the supplied "
                    "document information."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content


# =====================================================
# ACTIVE DOCUMENT
# =====================================================

def get_active_document():

    document_id = st.session_state.active_document

    if not document_id:
        return None

    return st.session_state.documents.get(document_id)


# =====================================================
# SIDEBAR — DOCUMENT HISTORY
# =====================================================

with st.sidebar:

    render_html("""
    <div class="history-heading">
        🐍 SNAKES AI
    </div>

    <div class="history-subtitle">
        Your Document Workspace
    </div>

    <div class="history-label">
        DOCUMENT HISTORY
    </div>
    """)

    documents = st.session_state.documents

    if not documents:

        st.caption("No documents uploaded yet.")

    else:

        sorted_documents = sorted(
            documents.items(),
            key=lambda item: item[1].get("created_at", ""),
            reverse=True
        )

        for document_id, document in sorted_documents:

            document_name = document.get(
                "name",
                "Untitled Document"
            )

            if len(document_name) > 25:
                document_name = document_name[:22] + "..."

            is_active = (
                document_id == st.session_state.active_document
            )

            label = (
                "●  " if is_active else "📄  "
            ) + document_name

            if st.button(
                label,
                key="history_" + document_id,
                use_container_width=True
            ):

                st.session_state.active_document = document_id
                st.rerun()

            if is_active:

                questions = document.get("questions", [])

                with st.expander(
                    "Question History (" + str(len(questions)) + ")"
                ):

                    if questions:

                        for item in reversed(questions):

                            st.markdown(
                                "**Q:** " + item.get("question", "")
                            )

                            st.markdown(
                                item.get("answer", "")
                            )

                            st.markdown("---")

                    else:

                        st.caption("No questions asked yet.")


# =====================================================
# MAIN HEADER
# =====================================================

render_html("""
<div class="main-header">

    <div class="snake">🐍</div>

    <div class="main-brand">
        SNAKES AI
    </div>

    <div class="main-title">
        Welcome to SNAKES AI
    </div>

    <div class="main-description">
        Document Intelligence Workspace
    </div>

</div>
""")


# =====================================================
# UPLOAD DOCUMENTS
# =====================================================

render_html("""
<div class="main-card">

    <div class="section-heading">
        Upload Documents
    </div>

    <div class="section-description">
        Upload your PDF document to analyze information
        and ask questions using AI.
    </div>

</div>
""")

uploaded_file = st.file_uploader(
    "Choose PDF document",
    type=["pdf"],
    label_visibility="collapsed",
    key="main_document_uploader"
)


# =====================================================
# SAVE DOCUMENT
# =====================================================

if uploaded_file is not None:

    file_bytes = uploaded_file.getvalue()

    document_id = hashlib.sha256(
        file_bytes
    ).hexdigest()

    if document_id not in st.session_state.documents:

        try:

            with st.spinner("Saving your document..."):

                document_text = extract_text_from_pdf(file_bytes)

                if not document_text.strip():

                    st.error(
                        "No readable text found in this PDF. "
                        "Please upload a text-based PDF."
                    )

                else:

                    pdf_path = os.path.join(
                        DOCUMENT_FOLDER,
                        document_id + ".pdf"
                    )

                    with open(pdf_path, "wb") as file:
                        file.write(file_bytes)

                    chunks = create_chunks(document_text)

                    st.session_state.documents[document_id] = {

                        "id": document_id,
                        "name": uploaded_file.name,
                        "pdf_path": pdf_path,
                        "text": document_text,
                        "chunks": chunks,
                        "feedback": None,
                        "analysis_complete": False,
                        "questions": [],
                        "created_at": datetime.now().isoformat()

                    }

                    save_history()

                    st.session_state.active_document = document_id

                    st.rerun()

        except Exception:

            st.error(
                "Unable to save this document. "
                "Please check the PDF and try again."
            )

    else:

        st.session_state.active_document = document_id

    document = get_active_document()

    if document:
        st.success("✓ Document uploaded successfully.")


# =====================================================
# ANALYZE DOCUMENT
# =====================================================

document = get_active_document()

if document:

    if not document.get("analysis_complete", False):

        if st.button(
            "Analyze Document",
            use_container_width=True
        ):

            try:

                with st.spinner(
                    "🐍 SNAKES AI is analyzing your document..."
                ):

                    feedback = analyze_document(
                        document["text"]
                    )

                    document["feedback"] = feedback
                    document["analysis_complete"] = True

                    save_history()

                st.success("Your document analysis is complete!")

                st.rerun()

            except Exception:

                st.error(
                    "Unable to analyze the document. "
                    "Please check your API settings and try again."
                )

    else:

        # =============================================
        # ANALYSIS RESULTS
        # =============================================

        st.markdown("---")

        render_html("""
        <div class="section-heading">
            Document Analysis
        </div>
        """)

        st.markdown(document["feedback"])

        st.download_button(
            "Download Analysis",
            data=document["feedback"],
            file_name="SNAKES_AI_Analysis.md",
            mime="text/markdown",
            use_container_width=True
        )

        # =============================================
        # ASK YOUR DOCUMENT
        # =============================================

        st.markdown("---")

        render_html("""
        <div class="section-heading">
            Ask Your Document
        </div>

        <div class="section-description">
            Ask any question related to your uploaded document.
            Get answers directly from its information.
        </div>
        """)

        with st.form("document_question_form"):

            question = st.text_input(
                "Search",
                placeholder="Ask something about your document..."
            )

            ask_button = st.form_submit_button(
                "Ask Question",
                use_container_width=True
            )

        if ask_button:

            if not question.strip():

                st.warning("Please enter your question.")

            else:

                try:

                    with st.spinner("Finding your answer..."):

                        answer = ask_document(
                            question,
                            document["chunks"]
                        )

                        document["questions"].append({

                            "question": question,
                            "answer": answer,
                            "created_at": datetime.now().isoformat()

                        })

                        save_history()

                    st.rerun()

                except Exception:

                    st.error(
                        "Unable to answer your question. "
                        "Please try again."
                    )

        # =============================================
        # PREVIOUS QUESTIONS
        # =============================================

        questions = document.get("questions", [])

        if questions:

            st.markdown("---")

            render_html("""
            <div class="section-heading">
                Previous Questions
            </div>
            """)

            for item in reversed(questions):

                with st.expander(item["question"]):

                    st.markdown(item["answer"])


else:

    render_html("""
    <div style="
        text-align:center;
        padding:25px;
        color:#888888;
        font-size:13px;
    ">
        Upload a document to get started.
    </div>
    """)


# =====================================================
# FOOTER
# =====================================================

render_html("""
<div class="footer-text">
    🐍 SNAKES AI
    <br><br>
    Document Intelligence Workspace
</div>
""")
