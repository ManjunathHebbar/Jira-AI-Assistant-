import sqlite3

DB_NAME = "database/jira_cache.db"



def initialize_database():

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS processed_tickets (
            issue_key TEXT PRIMARY KEY
        )
        """
    )

    connection.commit()
    connection.close()



def is_ticket_processed(issue_key):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "SELECT issue_key FROM processed_tickets WHERE issue_key = ?",
        (issue_key,)
    )

    result = cursor.fetchone()

    connection.close()

    return result is not None



def save_processed_ticket(issue_key):

    connection = sqlite3.connect(DB_NAME)

    cursor = connection.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO processed_tickets VALUES (?)",
        (issue_key,)
    )

    connection.commit()
    connection.close()