from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts):

    embedding = model.encode(texts)

    return embedding


if __name__ == "__main__":
    from src.app.rag.ingestion import extract_text_from_pdf, PROJECT_PATH
    from src.app.rag.chunking import chunk_pages

    pages = extract_text_from_pdf(
        PROJECT_PATH/"data"/"Financial Aid and Study Opportunities for Palestinian Students .pdf"
    )
    chunks = chunk_pages(pages)

    texts = [chunk["text"]
             for chunk in chunks]

    embeddings = embed_texts(texts)

    print("Chunks:", len(chunks))
    print("Embeddings shape:", embeddings.shape)
