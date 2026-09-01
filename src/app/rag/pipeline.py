from pathlib import Path

from app.rag.chunking import chunk_pages
from app.rag.embeddings import embed_texts
from app.rag.ingestion import extract_text_from_pdf
from app.rag.storage import insert_chunks, insert_document


def ingest_document(file_path):
    pages = extract_text_from_pdf(file_path)

    chunks = chunk_pages(pages)

    texts = [chunk["text"] for chunk in chunks]
    embeddings = embed_texts(texts)

    file_name = Path(file_path).name
    document_id = insert_document(file_name)

    insert_chunks(
        document_id=document_id,
        chunks=chunks,
        embeddings=embeddings,
    )

    return document_id


if __name__ == "__main__":
    document_id = ingest_document(
        "data/Financial Aid and Study Opportunities for Palestinian Students .pdf"
    )

    print("Stored document ID:", document_id)
