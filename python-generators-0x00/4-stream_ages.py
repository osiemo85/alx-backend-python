import mysql.connector

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
    except mysql.connector.Error as e:
        print(f"Error connecting to ALX_prodev database: {e}")
        return None

def stream_user_ages():
    """
    Generator that yields user ages one by one from the database.
    """
    connection = connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    
    for row in cursor:
        yield row['age']  # Yield the age one by one
    
    connection.close()

def calculate_average_age():
    """
    Function to calculate the average age of users using the stream_user_ages generator.
    """
    total_age = 0
    user_count = 0
    
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count == 0:
        return 0  # Avoid division by zero if no users exist
    
    return total_age / user_count

# Call the function to print the average age
average_age = calculate_average_age()
print(f"Average age of users: {average_age}")

