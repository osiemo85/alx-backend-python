import mysql.connector
import csv
from mysql.connector import Error
import uuid

# Function to connect to the MySQL database server
def connect_db():
    """
    Establish a connection to the MySQL server.
    Returns:
        connection (MySQLConnection): Connection object if successful, None otherwise.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="your_username",  # Replace with your MySQL username
            password="your_password"  # Replace with your MySQL password
        )
        print("Connected to MySQL server successfully.")
        return connection
    except Error as e:
        print(f"Error connecting to MySQL server: {e}")
        return None

# Function to create the database if it does not exist
def create_database(connection):
    """
    Create the ALX_prodev database if it does not already exist.
    Args:
        connection (MySQLConnection): Connection to the MySQL server.
    """
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        print("Database ALX_prodev created successfully (or already exists).")
        cursor.close()
    except Error as e:
        print(f"Error creating database: {e}")

# Function to connect to the ALX_prodev database
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
        print("Connected to the ALX_prodev database successfully.")
        return connection
    except Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

# Function to create the user_data table
def create_table(connection):
    """
    Create the user_data table in the ALX_prodev database if it does not already exist.
    Args:
        connection (MySQLConnection): Connection to the ALX_prodev database.
    """
    try:
        cursor = connection.cursor()
        create_table_query = """
        CREATE TABLE IF NOT EXISTS user_data (
            user_id CHAR(36) PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            email VARCHAR(255) NOT NULL,
            age DECIMAL(3, 0) NOT NULL
        )
        """
        cursor.execute(create_table_query)
        print("Table user_data created successfully (or already exists).")
        cursor.close()
    except Error as e:
        print(f"Error creating table: {e}")

# Function to insert data from a CSV file into the database
def insert_data(connection, csv_file):
    """
    Insert data from the CSV file into the user_data table.
    Args:
        connection (MySQLConnection): Connection to the ALX_prodev database.
        csv_file (str): Path to the CSV file containing user data.
    """
    try:
        cursor = connection.cursor()
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                user_id = str(uuid.uuid4())  # Generate a unique user_id
                name = row['name']
                email = row['email']
                age = row['age']
                # Insert data if it doesn't already exist
                cursor.execute("""
                INSERT INTO user_data (user_id, name, email, age)
                VALUES (%s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email), age=VALUES(age)
                """, (user_id, name, email, age))
        connection.commit()
        print("Data inserted into user_data table successfully.")
        cursor.close()
    except Error as e:
        print(f"Error inserting data: {e}")
    except FileNotFoundError:
        print(f"CSV file {csv_file} not found.")
