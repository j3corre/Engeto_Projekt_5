"""
main.py: čtvrtý projekt do Engeto Online Python Akademie - jednoduchý Task manager.

author: Jan Bláha
email: jan.blaha@bcas.cz
"""

def hlavni_menu():
    """Zobrazí hlavní menu aplikace."""

    print("\nSprávce úkolů - Hlavní menu")
    print("1. Přidat nový úkol")
    print("2. Zobrazit všechny úkoly")
    print("3. Odstranit úkol")
    print("4. Ukončit program")


def pridat_ukol(ukoly: list, nazev_ukolu: str, popis_ukolu: str):
    """Přidá nový úkol do seznamu úkolů.
    Args:
        ukoly (list): Předaný existující seznam úkolů.
        nazev_ukolu (str): Název nového úkolu.
        popis_ukolu (str): Popis nového úkolu.
    """
    
    if len(nazev_ukolu) == 0:
        print("Název úkolu nemůže být prázdný.")
        return

    if len(popis_ukolu) == 0:
        print("Popis úkolu nemůže být prázdný.")
        return
    
    ukoly.append({"nazev": nazev_ukolu, "popis": popis_ukolu})

    print(f"Úkol '{nazev_ukolu}' byl přidán.")


def zobrazit_ukoly(ukoly: list):
    """Zobrazí všechny úkoly v seznamu úkolů.
    Args:
        ukoly (list): Předaný existující seznam úkolů.
    """

    print("\nSeznam úkolů:")
    if not ukoly:
        print("Žádné úkoly k zobrazení.")
    for i, ukol in enumerate(ukoly, 1):
        print(f"{i}. {ukol['nazev']} - {ukol['popis']}")


def odstranit_ukol(ukoly: list, index: int) -> dict | None:
    """Odstraní úkol ze seznamu úkolů.
    Args:
        ukoly (list): Předaný existující seznam úkolů.
        index (int): Index úkolu k odstranění.
    """

    index -= 1  # Převod na nulový index

    if index < 0 or index >= len(ukoly):
        print("Neplatný index úkolu.")
        return None
    
    return ukoly.pop(index)

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

def main():
    """Hlavní funkce programu."""

    print("Vítejte v programu Task manager.")

    ukoly = []

    while True:
        hlavni_menu()
        volba = input("Vyberte možnost (1-4): ")

        match volba:
            case "1":
                nazev = input("Zadejte název úkolu: ")
                popis = input("Zadejte popis úkolu: ")
                pridat_ukol(ukoly, nazev, popis)
            case "2":
                zobrazit_ukoly(ukoly)
            case "3":
                if not ukoly:
                    print("\nŽádné úkoly k odstranění.")
                else:
                    zobrazit_ukoly(ukoly)
                    odstraneny_ukol = odstranit_ukol(ukoly, vrat_cislo("Zadejte číslo úkolu k odstranění: ", 1, len(ukoly)))
                    if odstraneny_ukol:
                        print(f"Úkol '{odstraneny_ukol['nazev']}' byl odstraněn.")
            case "4":
                print("\nKonec programu.")
                break
            case _:
                print("Neplatná volba, zkuste to znovu.")

if __name__ == "__main__":
    main()