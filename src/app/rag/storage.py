from app.db import get_connection


def insert_document(file_name):
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                insert into documents (file_name)
                values (%s)
                returning id;
                """,
                (file_name,),
            )
            document_id = cursor.fetchone()[0]
    connection.close()
    return document_id


def insert_chunks(document_id, chunks, embeddings):
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            for chunk_index, (chunk, embedding) in enumerate(
                zip(chunks, embeddings)
            ):
                cursor.execute(
                    """
                    INSERT INTO chunks (
                        document_id,
                        page_number,
                        chunk_index,
                        text,
                        embedding
                    )
                    VALUES (%s, %s, %s, %s, %s);
                    """,
                    (
                        document_id,
                        chunk["page_number"],
                        chunk_index,
                        chunk["text"],
                        embedding.tolist(),
                    ),
                )

    connection.close()


if __name__ == "__main__":
    document_id = insert_document("test.pdf")
    print("Document ID:", document_id)
