import sqlite3
import functools

# Decorator to log SQL queries
def log_queries():
    def decorator(func):
        @functools.wraps(func)  # Preserve the original function's metadata
        def wrapper(*args, **kwargs):
            # Log the query
            if args:
                print(f"Executing SQL Query: {args[0]}")
            else:
                print("No SQL query provided.")
            # Execute the original function
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log_queries()  # Apply the decorator
def fetch_all_users(query):
    """
    Connects to the database, executes the query, 
    fetches all rows, and then closes the connection.
    """
    conn = sqlite3.connect('users.db')  # Connect to the SQLite database
    cursor = conn.cursor()  # Create a cursor object
    cursor.execute(query)  # Execute the SQL query
    results = cursor.fetchall()  # Fetch all results
    conn.close()  # Close the connection
    return results  # Return the results

# Fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)
