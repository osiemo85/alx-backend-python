import mysql.connector
from mysql.connector import Error

def connect_to_prodev():
    """
    Connect to the ALX_prodev database.
    Returns:
        connection (MySQLConnection): Connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",
            password="your_password",
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def stream_users():
    """
    A generator that fetches rows from the user_data table one by one.
    Yields:
        dict: A dictionary containing user data for each row.
    """
    connection = connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)  # Use dictionary=True for row as a dict
            cursor.execute("SELECT * FROM user_data")
            for row in cursor:
                yield row  # Yield each row as a dictionary
            cursor.close()
        except Error as e:
            print(f"Error fetching rows: {e}")
        finally:
            connection.close()
    else:
        print("Connection to database failed.")

