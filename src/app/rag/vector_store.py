import numpy as np


def cosine_similarity(vector_a, vector_b):
    dot_product = np.dot(vector_a, vector_b)

    norm_a = np.linalg.norm(vector_a)
    norm_b = np.linalg.norm(vector_b)

    return dot_product / (norm_a * norm_b)


def search_similar_chunks(query_embedding, chunks, embeddings, top_k=3):
    results = []

    for chunk, embedding in zip(chunks, embeddings):
        score = cosine_similarity(query_embedding, embedding)

        results.append(
            {
                "score": score,
                "chunk": chunk,
            }
        )

    results.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return results[:top_k]


if __name__ == "__main__":
    from app.rag.chunking import chunk_pages
    from app.rag.embeddings import embed_texts
    from app.rag.ingestion import extract_text_from_pdf, PROJECT_PATH

    pages = extract_text_from_pdf(
        PROJECT_PATH
        / "data"
        / "Financial Aid and Study Opportunities for Palestinian Students .pdf"
    )

    chunks = chunk_pages(pages)

    texts = [chunk["text"] for chunk in chunks]
    chunk_embeddings = embed_texts(texts)

    question = "What scholarships are available for master's students?"

    query_embedding = embed_texts([question])[0]

    results = search_similar_chunks(
        query_embedding=query_embedding,
        chunks=chunks,
        embeddings=chunk_embeddings,
        top_k=3,
    )

    for result in results:
        print("Score:", result["score"])
        print("Page:", result["chunk"]["page_number"])
        print("Text:", result["chunk"]["text"])
        print("-" * 50)
