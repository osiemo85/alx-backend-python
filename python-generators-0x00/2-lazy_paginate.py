import mysql.connector
from mysql.connector import Error
import sys

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

def paginate_users(page_size, offset):
    """
    Fetch a page of users from the database with the given page_size and offset.
    
    Args:
        page_size (int): The number of rows to fetch in this page.
        offset (int): The offset to start fetching the next set of rows.
    
    Returns:
        list: A list of users (dict format) in this page.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def lazy_paginate(page_size):
    """
    Lazily fetch users in pages using a generator.
    
    Args:
        page_size (int): The number of rows to fetch in each page.
    
    Yields:
        list: A page of users as a list of dictionaries.
    """
    offset = 0
    while True:
        # Fetch the current page of users
        page = paginate_users(page_size, offset)
        
        # If no more users are returned, stop the generator
        if not page:
            break
        
        yield page  # Yield the current page of users
        
        offset += page_size  # Increment the offset for the next page
