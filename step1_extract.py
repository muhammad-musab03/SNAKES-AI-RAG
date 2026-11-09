# ============================================================
#  Resume Analyzer — STEP 1: Extract Text from a PDF
# ============================================================
#
#  RAG stands for: Retrieval-Augmented Generation
#
#  Before the AI can answer questions about a resume,
#  it must first be able to READ the resume.
#  PDFs are not plain text — we need a library to extract them.
#
#  Install:
#    pip install pdfplumber
#    python -m pip install pdfplumber
#
#  What you'll learn in this step:
#    ✔ How to open and read a PDF file in Python
#    ✔ How raw text looks after extraction
#    ✔ Why we need to "clean" text before using it
# ============================================================

import pdfplumber   # Library that reads PDF files


def extract_text_from_pdf(pdf_path):
    """
    Open a PDF file and extract all text from every page.

    pdfplumber opens the PDF like a book.
    We loop through each page and collect all the text.
    At the end we join everything into one big string.
    """
    all_text = []   # We'll store each page's text here

    # 'with' automatically closes the file when we're done
    with pdfplumber.open(pdf_path) as pdf:

        print(f"Total pages in PDF: {len(pdf.pages)}\n")

        for page_number, page in enumerate(pdf.pages, start=1):

            # .extract_text() reads the text on this page
            text = page.extract_text()

            if text:   # Some pages (images) may have no text
                all_text.append(text)
                print(f"  Page {page_number}: extracted {len(text)} characters")
            else:
                print(f"  Page {page_number}: no text found (might be an image)")

    # Join all pages with a blank line between them
    full_text = "\n\n".join(all_text)    #  ["page1", "page2", "page3"]  # full_text = "page1 /n/n page 2 /n/n page3"
    return full_text


def clean_text(text):
    """
    Clean up the raw extracted text.

    PDFs often have messy spacing and blank lines.
    This function tidies things up.
    """
    lines = text.split("\n")   # " data /n/n data // data"  >> line = [data1, data2, data3 ] 

    cleaned_lines = []
    for line in lines:
        line = line.strip()         # Remove leading/trailing spaces    # "   Nayab   " >> "Nayab"
        if line:                    # Skip completely empty lines
            cleaned_lines.append(line)

    cleaned_text = "\n".join(cleaned_lines)
    return cleaned_text


# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":

    # Change this to the path of your own resume PDF
    PDF_PATH = "testing_resume.pdf"

    print("=" * 55)
    print("  STEP 1: Extracting Text from Resume PDF")
    print("=" * 55 + "\n")

    # --- Extract ---
    raw_text = extract_text_from_pdf(PDF_PATH)

    print(f"\nRaw text length: {len(raw_text)} characters\n")

    # --- Clean ---
    clean = clean_text(raw_text)

    print("=" * 55)
    print("  Cleaned Text Preview:")
    print("=" * 55)
    print(clean)
    print("\n...")

    # --- Save to file so next steps can use it ---
    with open("resume_text.txt", "w", encoding="utf-8") as f:
        f.write(clean)

    print("\n✅ Text saved to: resume_text.txt")
    print("   (Next step will load this file)")
