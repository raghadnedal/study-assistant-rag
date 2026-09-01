import os
from dotenv import load_dotenv
import psycopg

load_dotenv()


def get_connection():
    DATABASE_URL = os.getenv("DATABASE_URL")

    connection = psycopg.connect(DATABASE_URL)

    return connection


if __name__ == "__main__":
    connection = get_connection()

    print("Connected to PostgreSQL")

    connection.close()
