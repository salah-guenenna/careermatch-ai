from pathlib import Path

import fitz


class UnsupportedDocumentError(ValueError):
    pass


def extract_pdf_text(path: Path) -> str:
    try:
        with fitz.open(path) as document:
            text = "\n".join(page.get_text() for page in document).strip()
    except Exception as exc:
        raise UnsupportedDocumentError("The uploaded file is not a readable PDF") from exc
    if not text:
        raise UnsupportedDocumentError("This PDF contains no selectable text. Scanned PDFs are not supported yet.")
    return text

