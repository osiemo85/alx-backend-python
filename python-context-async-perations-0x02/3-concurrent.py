import sqlite3
import aiosqlite
import asyncio

class DatabaseConnection:
    def __init__(self, db_name):
        """
        Initialize the DatabaseConnection with the name of the database file.
        :param db_name: Name or path of the database file.
        """
        self.db_name = db_name
        self.connection = None

    def __enter__(self):
        """
        Open a connection to the database and return the connection object.
        :return: sqlite3.Connection object
        """
        self.connection = sqlite3.connect(self.db_name)
        return self.connection

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the database connection is closed, even if an exception occurs.
        :param exc_type: Type of exception (if any)
        :param exc_value: Value of the exception (if any)
        :param traceback: Traceback object (if any)
        """
        if self.connection:
            self.connection.close()

class ExecuteQuery:
    def __init__(self, db_name, query, params=()):
        """
        Initialize the ExecuteQuery with database name, query, and parameters.
        :param db_name: Name or path of the database file.
        :param query: SQL query to execute.
        :param params: Parameters for the query.
        """
        self.db_name = db_name
        self.query = query
        self.params = params
        self.connection = None
        self.cursor = None

    def __enter__(self):
        """
        Open a connection to the database, prepare to execute the query, and return the cursor.
        :return: sqlite3.Cursor object
        """
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Ensure the cursor is closed and the database connection is committed and closed.
        :param exc_type: Type of exception (if any)
        :param exc_value: Value of the exception (if any)
        :param traceback: Traceback object (if any)
        """
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()

# Create a sample database and table for demonstration purposes
def setup_sample_db():
    with DatabaseConnection("sample.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                age INTEGER NOT NULL
            )
        """)
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Alice", "alice@example.com", 30))
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Bob", "bob@example.com", 20))
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Charlie", "charlie@example.com", 35))
        cursor.execute("INSERT INTO users (name, email, age) VALUES (?, ?, ?)", ("Dave", "dave@example.com", 45))
        conn.commit()

# Asynchronous functions for concurrent queries
async def async_fetch_users():
    async with aiosqlite.connect("sample.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            users = await cursor.fetchall()
            print("All users:")
            for user in users:
                print(user)

async def async_fetch_older_users():
    async with aiosqlite.connect("sample.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            older_users = await cursor.fetchall()
            print("Users older than 40:")
            for user in older_users:
                print(user)

async def fetch_concurrently():
    await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

if __name__ == "__main__":
    setup_sample_db()  # Set up the sample database
    print("Running concurrent database queries...")
    asyncio.run(fetch_concurrently())
