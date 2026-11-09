# SNAKES-AI-RAG
# 🐍 SNAKES AI – AI-Powered Document Assistant

**SNAKES AI** is a simple and intelligent document assistant built using Python and Retrieval-Augmented Generation (RAG).

It helps users understand PDF documents without reading every page manually.

Simply upload a PDF document, get an AI-generated summary, and ask questions about its content. SNAKES AI retrieves relevant information from the uploaded document and generates helpful answers.

---

## ✨ What Can SNAKES AI Do?

- 📄 **Upload PDF Documents:** Upload your PDF files for analysis.
- 📝 **Document Summarization:** Generate easy-to-understand summaries of uploaded documents.
- 💬 **Ask Questions:** Ask questions directly about your document.
- 🔍 **Information Retrieval:** Find relevant information from document content.
- 🤖 **AI-Powered Answers:** Get answers based on the information in your uploaded document.
- 📚 **Document Understanding:** Understand lengthy documents more easily.

---

## ⚙️ How Does It Work?

SNAKES AI works in two main steps:

### Step 1 – Analyze

The first step focuses on analyzing the document and preparing its information for the RAG workflow.

It helps process the document and organize its content so that relevant information can be retrieved when needed.

### Step 2 – Extract

The second step focuses on extracting relevant information from the processed document.

When a user asks a question, the system retrieves relevant document content and uses an AI model to generate an answer based on that information.

### Simple Workflow

1. Upload a PDF document.
2. The system processes the document.
3. Generate an AI-powered summary.
4. Ask a question about the document.
5. Retrieve relevant information.
6. Receive an AI-generated answer.

---

## 📁 Project Structure

```text
SNAKES-AI-RAG/
│
├── step1_analyze.py    # Document analysis
│
├── step2_extract.py    # Relevant information extraction
│
├── .env                # API key and environment settings
│
└── README.md           # Project documentation
```

---

## 🛠️ Technologies Used

- **Python** – Main programming language.
- **Retrieval-Augmented Generation (RAG)** – Connects document retrieval with AI-generated answers.
- **Groq API** – Provides access to the language model.
- **Streamlit** – Builds the interactive user interface.
- **PDF Processing** – Extracts information from PDF documents.
- **Large Language Models (LLMs)** – Generate summaries and answers.

---

## 🚀 Getting Started

Follow these simple steps to run SNAKES AI on your computer.

### 1. Install Python

Download and install Python from:

https://www.python.org/downloads/

### 2. Clone the Repository

Open your terminal or command prompt and run:

```bash
git clone https://github.com/YOUR-USERNAME/SNAKES-AI-RAG.git
```

Move into the project folder:

```bash
cd SNAKES-AI-RAG
```

### 3. Install Required Libraries

Install the required Python packages used by the project.

```bash
pip install streamlit groq python-dotenv pymupdf
```

If your code uses additional libraries, install those too.

### 4. Configure Your API Key

Create a file named `.env` in the main project folder.

Add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get your API key from:

https://console.groq.com/keys

**Important:** Replace `your_groq_api_key_here` with your actual API key.

Never share your API key publicly or upload your `.env` file to GitHub.

### 5. Run the Application

If `step1_analyze.py` contains the Streamlit application, run:

```bash
streamlit run step1_analyze.py
```

Open the local URL displayed in your terminal to access the application.

---

## 💡 How to Use SNAKES AI

Using SNAKES AI is simple:

1. Open the application in your browser.
2. Upload your PDF document.
3. Wait for the document processing to complete.
4. Generate and read the document summary.
5. Enter a question related to your document.
6. Get an AI-generated answer based on the document.

You can ask multiple questions about the same uploaded document.

---

## 🔐 Environment Variables

The project uses a `.env` file to store private configuration settings.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Keep this file private.

---

## 🎯 Project Goal

The main goal of SNAKES AI is to make reading, understanding, and searching through PDF documents easier.

Instead of manually searching through lengthy documents, users can upload their files, generate summaries, and ask questions to quickly find the information they need.

---

## 👨‍💻 Developer

**Muhammad Musab**

Artificial Intelligence | Generative AI | Python | LLMs

GitHub: https://github.com/in/rana-musab

---

## ⭐ Support

If you find this project useful, consider giving the repository a ⭐ on GitHub.

Thank you for checking out SNAKES AI! 🐍
