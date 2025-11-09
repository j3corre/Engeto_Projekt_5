import mysql.connector
from mysql.connector import Error
import pytest
from dotenv import load_dotenv
import os


def connect_to_db(host, user, password, database):
    try:
        return mysql.connector.connect(
            host=host, user=user, password=password, database=database
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
        cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS tasks (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                description VARCHAR(255) NOT NULL,
                state ENUM('pending', 'in_progress', 'completed') NOT NULL DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        )

        connection.commit()
        print(f"Database '{db_name}' and table 'tasks' initialized.")
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


@pytest.fixture(
    scope="module"
)  # Nastavíme scope pro celý modul, chceme smazat DB až na konci testů
def conn():
    # load .env.test konfiguracni data, pro TESTOVACI DB
    # zacatek

    load_dotenv(dotenv_path=".env.test")

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    init_database(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    print("\n☘️ FIXTURE - ZACATEK")

    # vraci data/funkci/object
    conn = connect_to_db(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
    print("\n☘️ FIXTURE - YIELD")
    yield conn

    # operace po vraceni
    clear_database(conn, DB_NAME)
    print("\n☘️ FIXTURE - CLOSE")
    conn.close()
