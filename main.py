"""
main.py: Pátý projekt do Engeto Online Python Akademie - vylepšený Task manager.

author: Jan Bláha
email: jan.blaha@bcas.cz
"""

from src.task_manager_db import *
from dotenv import load_dotenv
import os


def get_db_config():
    load_dotenv()

    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")

    return DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


def vrat_cislo(prompt: str, min_hodnota: int, max_hodnota: int) -> int:
    """Vrátí platné celé číslo zadané uživatelem v daném rozsahu.
    Args:
        prompt (str): Textová výzva pro uživatele.
        min_hodnota (int): Minimální povolená hodnota.
        max_hodnota (int): Maximální povolená hodnota.
    Returns:
        int: Platné celé číslo zadané uživatelem.
    """

    while True:
        try:
            cislo = int(input(prompt))
            if min_hodnota <= cislo <= max_hodnota:
                return cislo
            else:
                print(f"Prosím zadejte číslo mezi {min_hodnota} a {max_hodnota}.")
        except ValueError:
            print("Neplatný vstup. Zadejte prosím celé číslo.")


def stav_map(stav: str) -> str:
    """Převede stav úkolu (pending, in_progress, completed) na český výraz.
    Args:
        stav (str): Anglický stav úkolu.
    Returns:
        str: Český výraz pro stav úkolu.
    """
    mapping = {"pending": "nezahájeno", "in_progress": "probíhá", "completed": "hotovo"}
    return mapping.get(stav, "neznámý stav")


def hlavni_menu():
    """Zobrazí hlavní menu aplikace."""

    print("\nSprávce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit úkoly")
    print("3. Aktualizovat úkol")
    print("4. Odstranit úkol")
    print("5. Ukončit program")


def pridat_ukol(connection):
    """Přidá nový úkol do seznamu úkolů.
    Args:
        connection: Připojení k databázi.
    Returns:
        None
    """

    while not (nazev_ukolu := input("Zadejte název úkolu: ")):
        print("Název úkolu nemůže být prázdný.")
    if len(nazev_ukolu) > 100:  # omezení délky názvu na 100 znaků
        print("Název úkolu je příliš dlouhý. Bude zkrácen na maximálně 100 znaků.")
        nazev_ukolu = nazev_ukolu[:100]

    while not (popis_ukolu := input("Zadejte popis úkolu: ")):
        print("Popis úkolu nemůže být prázdný.")
    if len(popis_ukolu) > 255:  # omezení délky popisu na 255 znaků
        print("Popis úkolu je příliš dlouhý. Bude zkrácen na maximálně 255 znaků.")
        popis_ukolu = popis_ukolu[:255]

    add_task(connection, nazev_ukolu, popis_ukolu, "pending")

    print(f"Úkol '{nazev_ukolu}' byl přidán.")


def zobrazit_ukoly(connection, caption: str = "\nSeznam úkolů:"):
    """Zobrazí všechny úkoly v seznamu úkolů.
    Args:
        connection: Připojení k databázi.
    Returns:
        dict: Seznam úkolů.
    """

    tasks = get_tasks(connection)
    print(caption)
    if not tasks:
        print("Žádné úkoly k zobrazení.")

    for i, task in enumerate(tasks, 1):
        print(
            f"{i}. {task['name']} - {task['description']} ({stav_map(task['state'])}) z {task['created_at']}"
        )
    return tasks


def aktualizovat_ukol(connection):
    """Aktualizuje stav vybraného úkolu.
    Args:
        connection: Připojení k databázi.
    Returns:
        None
    """
    tasks = zobrazit_ukoly(connection, "\nSeznam úkolů k aktualizaci:")

    if not tasks:
        print("Žádné úkoly k aktualizaci.")
        return

    index = vrat_cislo("Zadejte číslo úkolu k aktualizaci: ", 1, len(tasks)) - 1
    if 0 <= index < len(tasks):
        print(f"Zadejte nový stav úkolu {tasks[index]['name']}:")
        print("1. Probíhající")
        print("2. Dokončený")
        novy_stav = vrat_cislo("Vyberte možnost (1-2): ", 1, 2)
        stav = {1: "in_progress", 2: "completed"}

        if stav[novy_stav]:
            update_task_state(connection, tasks[index]["id"], stav[novy_stav])
            print(f"Úkol '{tasks[index]['name']}' byl aktualizován.")
        else:
            print("Neplatný stav úkolu.")
    else:
        print("Neplatný výběr úkolu.")


def odstranit_ukol(connection):
    """ "
    Odstraní vybraný úkol ze seznamu úkolů.
    Args:
        connection: Připojení k databázi.
    Returns:
        None
    """
    tasks = zobrazit_ukoly(connection, "\nSeznam úkolů k odstranění:")

    if not tasks:
        print("Žádné úkoly k odstranění.")
        return

    index = vrat_cislo("Zadejte číslo úkolu k odstranění: ", 1, len(tasks)) - 1
    if 0 <= index < len(tasks):
        delete_task(connection, tasks[index]["id"])
        print(f"Úkol '{tasks[index]['name']}' byl odstraněn.")
    else:
        print("Neplatný výběr úkolu.")


def main():
    """Hlavní funkce programu."""

    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME = (
        get_db_config()
    )  # Načtení konfigurace databáze z .env souboru

    print("Vítejte v programu Task manager.")

    # Připojení k databázi
    try:
        conn = connect_to_database(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )
    except ConnectionError:  # pokud připojení selže, inicializujeme databázi
        initialize_database(
            DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
        )  # Inicializace databáze a tabulky úkolů
        conn = connect_to_database(
            host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME
        )

    #
    while True:
        hlavni_menu()
        volba = input("Vyberte možnost (1-5): ")

        match volba:
            case "1":
                pridat_ukol(conn)
            case "2":
                zobrazit_ukoly(conn)
            case "3":
                aktualizovat_ukol(conn)
            case "4":
                odstranit_ukol(conn)
            case "5":
                print("\nKonec programu.")
                break
            case _:
                print("Neplatná volba, zkuste to znovu.")

    # Uzavření připojení k databázi
    close_connection(conn)


if __name__ == "__main__":
    main()
