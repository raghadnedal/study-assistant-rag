def chunk_pages(pages, chunk_size=500, chunk_overlap=50):
    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page_number"]

        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append(
                {
                    "page_number": page_number,
                    "text": chunk_text,
                }
            )

            start += chunk_size - chunk_overlap

    return chunks


if __name__ == "__main__":
    from app.rag.ingestion import extract_text_from_pdf, PROJECT_PATH

    pages = extract_text_from_pdf(
        PROJECT_PATH
        / "data"
        / "Financial Aid and Study Opportunities for Palestinian Students .pdf"
    )

    chunks = chunk_pages(pages)

    print("Number of chunks:", len(chunks))
    print(chunks[0])
    print(chunks[1])
