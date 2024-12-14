import sqlite3

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

# Create a sample database and table for demonstration purposes
def setup_sample_db():
    with DatabaseConnection("sample.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Alice", "alice@example.com"))
        cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Bob", "bob@example.com"))
        conn.commit()

# Query the database using the context manager
def query_users():
    with DatabaseConnection("sample.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)

if __name__ == "__main__":
    setup_sample_db()  # Set up the sample database
    print("Users in the database:")
    query_users()  # Query and print the users
