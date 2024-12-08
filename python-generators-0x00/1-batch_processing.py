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
            user="your_username",  # Replace with your MySQL username
            password="your_password",  # Replace with your MySQL password
            database="ALX_prodev"
        )
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def stream_users_in_batches(batch_size):
    """
    A generator that fetches rows from the user_data table in batches.
    
    Args:
        batch_size (int): The number of rows to fetch in each batch.
    
    Yields:
        list: A batch of user data rows (list of dictionaries).
    """
    connection = connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            
            # Loop to fetch rows in batches
            while True:
                batch = cursor.fetchmany(batch_size)  # Fetch next batch of rows
                if not batch:
                    break  # Exit if no more rows
                yield batch  # Yield the batch of rows
            
            cursor.close()
        except Error as e:
            print(f"Error fetching rows in batches: {e}")
        finally:
            connection.close()
    else:
        print("Connection to database failed.")

def batch_processing(batch_size):
    """
    Processes user data in batches and filters users over the age of 25.
    
    Args:
        batch_size (int): The size of each batch to process.
    """
    for batch in stream_users_in_batches(batch_size):
        # Filter users older than 25
        filtered_users = [user for user in batch if user['age'] > 25]
        
        # Process the filtered users (e.g., print them)
        for user in filtered_users:
            print(user)
