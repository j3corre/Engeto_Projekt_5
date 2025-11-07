import mysql.connector
from mysql.connector import Error

def connect_to_db(host, user, password, database):
    try:
        return mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
    except Error as e:
        raise ConnectionError(f"Database connection failed: {e}")

def initialize_database(host, user, password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.database = db_name

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                age INT NOT NULL CHECK (age >= 0),
                email VARCHAR(255) DEFAULT NULL
            )
        """)

        connection.commit()
        print(f"Database '{db_name}' and table 'users' initialized.")
    except Error as e:
        raise RuntimeError(f"Database initialization failed: {e}")
    finally:
        if connection:
            connection.close()

def add_user(connection, name, age, email=None):
    if not connection:
        raise RuntimeError("No database connection.")
    if not name:
        raise ValueError("Invalid user name.")
    if age < 0:
        raise ValueError("Invalid user age.")

    cursor = connection.cursor()

    if email:
        cursor.execute(
            "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)",
            (name, age, email)
        )
    else:
        cursor.execute(
            "INSERT INTO users (name, age) VALUES (%s, %s)",
            (name, age)
        )

    connection.commit()

def get_users(connection):
    if not connection:
        raise RuntimeError("No database connection.")
    cursor = connection.cursor()
    cursor.execute("SELECT name, age, email FROM users")
    return cursor.fetchall()

def close_connection(connection):
    if connection:
        connection.close()
