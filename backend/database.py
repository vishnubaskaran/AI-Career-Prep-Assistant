import sqlite3


def create_database():

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS progress (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT,
            skill TEXT,
            completed INTEGER
        )
    """)

    connection.commit()

    print("✅ Database and progress table created successfully!")

    connection.close()


def save_progress(company, skill, completed):

    connection = sqlite3.connect("placement.db")

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO progress (company, skill, completed)
        VALUES (?, ?, ?)
    """, (company, skill, completed))

    connection.commit()

    connection.close()


create_database()