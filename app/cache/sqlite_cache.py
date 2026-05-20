import sqlite3
import os
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DB_NAME = str(PROJECT_ROOT / "cache" / "processed_tickets.db")
PROCESSING_LOCK_TTL_SECONDS = 1800


def connect_database():

    connection = sqlite3.connect(
        DB_NAME,
        timeout=30
    )

    connection.execute("PRAGMA journal_mode=WAL")

    connection.execute("PRAGMA busy_timeout=30000")

    return connection


def initialize_database():

    os.makedirs(
        os.path.dirname(DB_NAME),
        exist_ok=True
    )

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_tickets (
            issue_key TEXT PRIMARY KEY,
            content_hash TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processing_tickets (
            issue_key TEXT PRIMARY KEY,
            content_hash TEXT,
            claimed_at REAL
        )
        """
    )

    cursor.execute("PRAGMA table_info(processing_tickets)")

    columns = [
        row[1]
        for row in cursor.fetchall()
    ]

    if "claimed_at" not in columns:

        cursor.execute(
            """
            ALTER TABLE processing_tickets
            ADD COLUMN claimed_at REAL
            """
        )

    connection.commit()

    connection.close()


def should_process_ticket(
    issue_key,
    new_hash
):

    connection = connect_database()

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


def claim_ticket_for_processing(
    issue_key,
    new_hash
):

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute("BEGIN IMMEDIATE")

    cursor.execute(
        """
        SELECT content_hash
        FROM processed_tickets
        WHERE issue_key = ?
        """,
        (issue_key,)
    )

    processed_row = cursor.fetchone()

    if processed_row and processed_row[0] == new_hash:

        connection.commit()

        connection.close()

        return False

    now = time.time()

    cursor.execute(
        """
        SELECT content_hash, claimed_at
        FROM processing_tickets
        WHERE issue_key = ?
        """,
        (issue_key,)
    )

    processing_row = cursor.fetchone()

    if processing_row and processing_row[0] == new_hash:

        claimed_at = processing_row[1] or 0

        lock_age = now - claimed_at

        if lock_age < PROCESSING_LOCK_TTL_SECONDS:

            connection.commit()

            connection.close()

            return False

    cursor.execute(
        """
        INSERT OR REPLACE INTO processing_tickets
        (issue_key, content_hash, claimed_at)
        VALUES (?, ?, ?)
        """,
        (
            issue_key,
            new_hash,
            now
        )
    )

    connection.commit()

    connection.close()

    return True


def save_processed_ticket(
    issue_key,
    content_hash
):

    connection = connect_database()

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

    cursor.execute(
        """
        DELETE FROM processing_tickets
        WHERE issue_key = ?
        """,
        (issue_key,)
    )

    connection.commit()

    connection.close()


def clear_processing_ticket(
    issue_key,
    content_hash
):

    connection = connect_database()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM processing_tickets
        WHERE issue_key = ?
        AND content_hash = ?
        """,
        (
            issue_key,
            content_hash
        )
    )

    connection.commit()

    connection.close()
