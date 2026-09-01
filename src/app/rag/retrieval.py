from app.db import get_connection
from app.rag.embeddings import embed_texts


def retrieve_chunks(question, top_k=5):
    query_embedding = embed_texts([question])[0].tolist()

    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    chunks.text,
                    chunks.page_number,
                    documents.file_name,
                    chunks.embedding <=> %s::vector AS distance
                FROM chunks
                JOIN documents
                    ON chunks.document_id = documents.id
                ORDER BY chunks.embedding <=> %s::vector
                LIMIT %s;
                """,
                (
                    query_embedding,
                    query_embedding,
                    top_k,
                ),
            )

            rows = cursor.fetchall()

    connection.close()

    results = []

    for row in rows:

        results.append(
            {
                "text": row[0],
                "page_number": row[1],
                "file_name": row[2],
                "distance": row[3],
            }
        )

    return results


def build_context(results):
    context_parts = []

    for result in results:
        context_parts.append(
            f"""
            Source:{result["file_name"]}
            Page: {result["page_number"]}

            Content:
            {result["text"]}
            """
        )

    return "\n".join(context_parts)


if __name__ == "__main__":
    results = retrieve_chunks(
        "What scholarships are available for master's students?",
        top_k=3,
    )

    for result in results:
        print(result)
