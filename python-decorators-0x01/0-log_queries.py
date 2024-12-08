import sqlite3
import functools

def log_queries():
    """
    A decorator to log the SQL queries executed by any function.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Assuming the first argument to the function is the query
            query = args[0] if args else kwargs.get('query', 'Unknown query')
            print(f"Executing SQL Query: {query}")
            result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@log_queries()
def fetch_all_users(query):
    """
    Fetch all users from the database based on the query.
    """
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
