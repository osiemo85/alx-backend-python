import sqlite3
import functools

def with_db_connection(func):
    """
    A decorator that opens a database connection, passes it to the function,
    and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Establish a database connection
        conn = sqlite3.connect('users.db')
        try:
            # Pass the connection as the first argument to the function
            return func(conn, *args, **kwargs)
        finally:
            # Ensure the connection is closed after the function executes
            conn.close()
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """
    Fetch a user by ID from the database.
    """
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

# Fetch user by ID with automatic connection handling
user = get_user_by_id(user_id=1)
print(user)

