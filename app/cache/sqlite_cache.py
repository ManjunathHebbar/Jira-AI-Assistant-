import sqlite3
import os

DB_NAME = "cache/processed_tickets.db"


def initialize_database():

    os.makedirs("cache", exist_ok=True)

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_tickets (
            issue_key TEXT PRIMARY KEY,
            content_hash TEXT
        )
        """
    )

    connection.commit()

    connection.close()


def should_process_ticket(
    issue_key,
    new_hash
):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT content_hash
        FROM processed_tickets
        WHERE issue_key = ?
        """,
        (issue_key,)
    )

    row = cursor.fetchone()

    connection.close()

    if not row:

        return True

    old_hash = row[0]

    return old_hash != new_hash


def save_processed_ticket(
    issue_key,
    content_hash
):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO processed_tickets
        (issue_key, content_hash)
        VALUES (?, ?)
        """,
        (
            issue_key,
            content_hash
        )
    )

    connection.commit()

    connection.close()