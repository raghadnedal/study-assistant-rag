from pathlib import Path

from pypdf import PdfReader


PROJECT_PATH = Path(__file__).resolve().parents[3]


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text


def extract_text_from_pdf(file_path):
    reader = PdfReader(file_path)
    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = clean_text(text=text)

        pages.append(
            {
                "page_number": page_number,
                "text": text,
            }
        )

    return pages


if __name__ == "__main__":
    pages = extract_text_from_pdf(
        PROJECT_PATH
        / "data"
        / "Financial Aid and Study Opportunities for Palestinian Students .pdf"
    )

    print(pages[1])
