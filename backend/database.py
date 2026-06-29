from postgres_db import get_connection


def create_database():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id SERIAL PRIMARY KEY,
            company TEXT,
            skill TEXT,
            completed BOOLEAN
        )
    """)

    connection.commit()

    cursor.close()

    connection.close()

    print("✅ PostgreSQL database initialized!")


def save_progress(company, skill, completed):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO progress
        (company, skill, completed)
        VALUES (%s, %s, %s)
        """,
        (company, skill, completed)
    )

    connection.commit()

    cursor.close()

    connection.close()


create_database()