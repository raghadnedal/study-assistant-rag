from uuid import uuid4
from app.db import get_connection


def create_session():
    session_id = uuid4()
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
        insert into chat_sessions(id)
        values(%s)
        """,
                (session_id,),
            )
    connection.close()
    return str(session_id)


def save_message(session_id, role, content):
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                insert into chat_messages(
                session_id,
                role,
                content
                )
                values(
                %s,%s,%s)
                """,
                (session_id, role, content),
            )
    connection.close()


def get_history(session_id):
    connection = get_connection()
    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                select role,content
                from chat_messages
                where session_id = %s
                order by created_at ASC, id ASC;
                """,
                (session_id,),
            )
            rows = cursor.fetchall()
    connection.close()
    history = []
    for row in rows:
        history.append(
            {
                "role": row[0],
                "content": row[1],
            }
        )
    return history


def session_exists(session_id):
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM chat_sessions
                WHERE id = %s;
                """,
                (session_id,),
            )

            row = cursor.fetchone()

    connection.close()

    return row is not None


def document_exists(document_id):
    connection = get_connection()

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT 1
                FROM documents
                WHERE id = %s;
                """,
                (document_id,),
            )

            row = cursor.fetchone()

    connection.close()

    return row is not None
