#### ZDE BUDOU TESTY #### 
from src.db_mysql import add_user, get_users
import pytest

@pytest.mark.parametrize(
        "name, age, email",
        [
            ("Petr", 18, "petr@svetr.cz"),
            ("Rene", 50, "rene@svetr.cz"),
            ("Rudolf", 43, "rudolf@svetr.cz"),
            ("Karel", 33, None),
        ]
)
def test_add_user_happy_flow(conn, name, age, email):
    # zavolat funkci add_user()
    add_user(conn, name, age, email)

    # vlastni volani do DB a overeni, ze se uzivatel pridal
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT id, name, age, email FROM users WHERE name = %s AND age = %s", (name, age))
    users = cursor.fetchall()
    user = users[0]

    print(user)

    # kontrola, zda dany uzivatel existuje
    assert user != None, f"Ocekavame ze se nam vrati uzivatel {name} ve veku {age}"
    assert user['name'] == name
    assert user['age'] == age


@pytest.mark.parametrize(
        "name, age, email, error_type, error_message",
        [
            (None, 18, "petr@svetr.cz", ValueError, "Invalid user name."),
            ("Rene", -20, "rene@svetr.cz", ValueError, "Invalid user age."),
        ]
)
def test_add_user_fail_flow(conn, name, age, email, error_type, error_message):
    # zavolame funkci add_user s neplatnymi parametry
    with pytest.raises(error_type) as error:
        add_user(conn, name, age, email)

    assert str(error.value) == error_message, f"Ocekavame chybovou hlasku {error_message}, ale dostali jsme {str(error.value)}"



def test_add_user_fixure(conn):
    # zavolat funkci add_user()
    print("\n☘️ FUNC - ADD USER")
    add_user(conn, "Fixator", 12)

    # vlastni volani do DB a overeni, ze se uzivatel pridal
    cursor = conn.cursor(dictionary=True)
    cursor.execute(f"SELECT id, name, age, email FROM users WHERE name = %s AND age = %s", ("Fixator", 12))
    users = cursor.fetchall()
    user = users[0]

    print(user)

    # kontrola, zda dany uzivatel existuje
    assert user != None, f"Ocekavame ze se nam vrati uzivatel {"Fixator"} ve veku {12}"