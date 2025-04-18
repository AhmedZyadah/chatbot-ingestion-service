
import fitz  # PyMuPDF

def extract_text_by_page(file_path: str):
    doc = fitz.open(file_path)
    results = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")
        results.append({
            "page": page_num + 1,
            "text": text.strip()
        })

    return results
