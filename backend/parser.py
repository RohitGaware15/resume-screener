import fitz  # PyMuPDF
import io


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract plain text from PDF bytes."""
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    doc.close()
    return text.strip()


def extract_text_from_multiple(files: list[tuple[str, bytes]]) -> list[tuple[str, str]]:
    """
    files: list of (filename, bytes)
    returns: list of (filename, extracted_text)
    """
    results = []
    for filename, content in files:
        try:
            text = extract_text_from_pdf(content)
            results.append((filename, text))
        except Exception as e:
            results.append((filename, f"[ERROR extracting text: {e}]"))
    return results
