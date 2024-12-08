import sqlite3
import functools

# Dictionary to store cached query results
query_cache = {}

def cache_query(func):
    """
    A decorator that caches query results to avoid redundant database calls.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from the arguments
        query = kwargs.get('query') or args[1]
        
        # Check if the query is already in the cache
        if query in query_cache:
            print("Using cached result for query:", query)
            return query_cache[query]
        
        # Execute the function and cache the result
        print("Executing query and caching result:", query)
        result = func(*args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

def with_db_connection(func):
    """
    A decorator that opens a database connection, passes it to the function,
    and closes it afterward.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            return func(conn, *args, **kwargs)
        finally:
            conn.close()
    return wrapper

@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """
    Fetch users from the database and cache the results of the query.
    """
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

# First call will execute the query and cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")
print(users)

# Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")
print(users_again)

