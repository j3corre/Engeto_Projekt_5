"""
task_manager_db.py: Modul pro správu databáze úkolů pomocí MySQL.
Poskytuje funkce pro připojení k databázi, inicializaci tabulky úkolů,
přidání, získání, aktualizaci a odstranění úkolů.

Author: Jan Bláha
Email: jan.blaha@bcas.cz
"""

import mysql.connector
from mysql.connector import Error


def connect_to_database(host, user, password, database):
    """Připojí se k databázi MySQL.
    Args:
        host (str): Adresa hostitele databáze.
        user (str): Uživatelské jméno pro připojení k databázi.
        password (str): Heslo pro připojení k databázi.
        database (str): Název databáze.
    Returns:
        connection: Objekt připojení k databázi.
    Raises:
        ConnectionError: Pokud se připojení nezdaří.
    """

    try:
        return mysql.connector.connect(
            host=host, user=user, password=password, database=database
        )
    except Error as e:
        raise ConnectionError(f"Database connection failed: {e}")


def initialize_database(host, user, password, db_name):
    """Inicializuje databázi a tabulku úkolů, pokud neexistují.
    Args:
        host (str): Adresa hostitele databáze.
        user (str): Uživatelské jméno pro připojení k databázi.
        password (str): Heslo pro připojení k databázi.
        db_name (str): Název databáze.
    Raises:
        RuntimeError: Pokud inicializace databáze selže.
    """

    try:
        connection = mysql.connector.connect(host=host, user=user, password=password)

        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
        connection.database = db_name

        cursor.execute(
            """
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


def add_task(connection, name, description, state):
    """Přidá nový úkol do tabulky úkolů.
    Args:
        connection: Připojení k databázi.
        name (str): Název úkolu.
        description (str): Popis úkolu.
        state (str): Stav úkolu ('pending', 'in_progress', 'completed').
    Raises:
        RuntimeError: Pokud přidání úkolu selže.
        ValueError: Pokud jsou zadané neplatné hodnoty.
    """

    if not connection:
        raise RuntimeError("No database connection.")
    if not name:
        raise ValueError("Invalid task name.")
    if not description:
        raise ValueError("Invalid task description.")
    if state not in ["pending", "in_progress", "completed"]:
        raise ValueError("Invalid task state.")
    if len(name) > 100:
        raise ValueError("Task name is too long.")
    if len(description) > 255:
        raise ValueError("Task description is too long.")

    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO tasks (name, description, state) VALUES (%s, %s, %s)",
        (name, description, state),
    )
    connection.commit()


def get_tasks(connection):
    """Vrátí seznam všech úkolů v databázi.
    Args:
        connection: Připojení k databázi.
    Returns:
        dict: Seznam úkolů.
    Raises:
        RuntimeError: Pokud není k dispozici připojení k databázi.
    """

    if not connection:
        raise RuntimeError("No database connection.")
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, name, description, state, created_at FROM tasks ORDER BY created_at ASC"
    )
    return cursor.fetchall()


def update_task_state(connection, task_id, new_state):
    """Aktualizuje stav úkolu v databázi.
    Args:
        connection: Připojení k databázi.
        task_id (int): ID úkolu.
        new_state (str): Nový stav úkolu.
    Raises:
        RuntimeError: Pokud není k dispozici připojení k databázi.
        ValueError: Pokud je zadaný neplatný stav úkolu.
    """

    if not connection:
        raise RuntimeError("No database connection.")
    if new_state not in ["pending", "in_progress", "completed"]:
        raise ValueError("Invalid task state.")
    if task_id not in { # kontrola platného ID úkolu
        task["id"] for task in get_tasks(connection)
    }:
        raise ValueError("Invalid task ID.")

    cursor = connection.cursor()
    cursor.execute("UPDATE tasks SET state = %s WHERE id = %s", (new_state, task_id))
    connection.commit()


def delete_task(connection, task_id):
    """Odstraní úkol z databáze.
    Args:
        connection: Připojení k databázi.
        task_id (int): ID úkolu.
    Raises:
        RuntimeError: Pokud není k dispozici připojení k databázi.
    """

    if not connection:
        raise RuntimeError("No database connection.")
    if task_id not in { # kontrola platného ID úkolu
        task["id"] for task in get_tasks(connection)
    }:  
        raise ValueError("Invalid task ID.")

    cursor = connection.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    connection.commit()


def close_connection(connection):
    """Uzavře připojení k databázi.
    Args:
        connection: Připojení k databázi.
    """

    if connection:
        connection.close()
