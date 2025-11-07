import mysql.connector
from mysql.connector import Error
import pytest

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

def init_database(host, user, password, db_name):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
        )

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.database = db_name
        cursor.execute(f"""
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

def clear_database(conn, db_name):
    cursor = conn.cursor()
    cursor.execute(f"DROP DATABASE {db_name}")
    conn.commit()
    cursor.close()


@pytest.fixture(scope="function")
def conn():

    # load .env konfiguracni data, pro TESTOVACI DB
    # zacatek
    init_database("localhost", "root", "1111", "engeto_test")
    print("\n☘️ FIXTURE - ZACATEK")

    # vraci data/funkci/object
    conn = connect_to_db("localhost", "root", "1111", "engeto_test")
    print("\n☘️ FIXTURE - YIELD")
    yield conn

    # operace po vraceni
    clear_database(conn, "engeto_test" )
    print("\n☘️ FIXTURE - CLOSE")
    conn.close()