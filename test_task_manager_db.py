#### ZDE BUDOU TESTY ####
from src.task_manager_db import add_task, get_tasks, update_task_state, delete_task
import pytest


@pytest.mark.testAddTask
@pytest.mark.parametrize(
    "name, description, state",
    [
        ("První úkol", "Popis úkolu 1", "pending"),
        ("Druhý úkol", "Popis úkolu 2", "in_progress"),
        ("Třetí úkol", "Popis úkolu 3", "completed"),
        ("Čtvrtý úkol", "Popis úkolu 4", "pending"),
    ],
)
def test_add_task_happy_flow(conn, name, description, state):
    # zavolat funkci add_task()
    add_task(conn, name, description, state)

    # vlastní volání do DB a ověření, že se úkol přidal
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT id, name, description, state FROM tasks WHERE name = %s AND description = %s",
        (name, description),
    )
    tasks = cursor.fetchall()
    task = tasks[0]

    print(task)

    # kontrola, zda daný úkol existuje
    assert (
        task != None
    ), f"Očekáváme, že se nám vrátí úkol {name} s popisem {description} a stavem {state}"
    assert task["name"] == name
    assert task["description"] == description
    assert task["state"] == state


@pytest.mark.parametrize(
    "name, description, state, error_type, error_message",
    [
        ("", "Úkol bez názvu", "pending", ValueError, "Invalid task name."),
        ("Úkol bez popisu", "", "in_progress", ValueError, "Invalid task description."),
        (
            "Příliš dlouhý název úkolu" * 10,
            "Dlouhý název úkolu" * 10,
            "completed",
            ValueError,
            "Task name is too long.",
        ),
        (
            "Dlouhý popis",
            "Velmi dlouhý popis úkolu" * 25,
            "pending",
            ValueError,
            "Task description is too long.",
        ),
        (
            "Špatný stav",
            "Neplatný stav úkolu",
            "invalid_state",
            ValueError,
            "Invalid task state.",
        ),
    ],
)
def test_add_task_fail_flow(conn, name, description, state, error_type, error_message):
    # zavolame funkci add_task s neplatnymi parametry
    with pytest.raises(error_type) as error:
        add_task(conn, name, description, state)

    assert (
        str(error.value) == error_message
    ), f"Očekáváme chybovou hlášku {error_message}, ale dostali jsme {str(error.value)}"


@pytest.mark.testGetTasks
def test_get_tasks_ok(conn):
    add_task(conn, "Úkol 1", "Popis 1", "pending")
    get_tasks_list = get_tasks(conn)

    assert (
        len(get_tasks_list) >= 1
    ), f"Očekáváme alespoň 1 úkol v databázi, ale dostali jsme {len(get_tasks_list)}"
    assert get_tasks_list[-1]["name"] == "Úkol 1"
    assert get_tasks_list[-1]["description"] == "Popis 1"
    assert get_tasks_list[-1]["state"] == "pending"


@pytest.mark.testGetTasks
def test_get_tasks_no_connection():
    with pytest.raises(RuntimeError) as error:
        get_tasks(None)
    assert (
        str(error.value) == "No database connection."
    ), f"Očekáváme chybovou hlášku 'No database connection.', ale dostali jsme {str(error.value)}"


@pytest.mark.testUpdateTaskState
@pytest.mark.parametrize(
    "name, description, state, new_state",
    [
        (
            "První úkol pro změnu stavu",
            "Popis úkolu 1 pro změnu stavu",
            "pending",
            "in_progress",
        ),
        (
            "Druhý úkol pro změnu stavu",
            "Popis úkolu 2 pro změnu stavu",
            "in_progress",
            "completed",
        ),
        (
            "Třetí úkol pro změnu stavu",
            "Popis úkolu 3 pro změnu stavu",
            "completed",
            "pending",
        ),
    ],
)
def test_update_task_state_ok(conn, name, description, state, new_state):
    # přidáme úkol ve stavu čekající
    add_task(conn, name, description, state)

    # získat ID přidaného úkolu
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT id FROM tasks WHERE name = %s AND description = %s",
        (name, description),
    )
    task = cursor.fetchone()
    task_id = task["id"]

    # aktualizovat stav úkolu
    update_task_state(conn, task_id, new_state)

    # ověřit, že se stav úkolu změnil
    cursor.execute(f"SELECT state FROM tasks WHERE id = %s", (task_id,))
    updated_task = cursor.fetchone()

    assert (
        updated_task["state"] == new_state
    ), f"Očekáváme, že stav úkolu bude '{new_state}', ale je {updated_task['state']}"


@pytest.mark.testUpdateTaskState
def test_update_task_state_no_connection():
    with pytest.raises(RuntimeError) as error:
        update_task_state(None, 1, "completed")
    assert (
        str(error.value) == "No database connection."
    ), f"Očekáváme chybovou hlášku 'No database connection.', ale dostali jsme {str(error.value)}"


@pytest.mark.testUpdateTaskState
def test_update_task_state_invalid_state(conn):
    # přidáme úkol ve stavu čekající
    add_task(conn, "Úkol pro neplatný stav", "Popis úkolu pro neplatný stav", "pending")

    # získat ID přidaného úkolu
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT id FROM tasks WHERE name = %s AND description = %s",
        ("Úkol pro neplatný stav", "Popis úkolu pro neplatný stav"),
    )
    task = cursor.fetchone()
    task_id = task["id"]

    with pytest.raises(ValueError) as error:
        update_task_state(conn, task_id, "invalid_state")
    assert (
        str(error.value) == "Invalid task state."
    ), f"Očekáváme chybovou hlášku 'Invalid task state.', ale dostali jsme {str(error.value)}"


@pytest.mark.testUpdateTaskState
def test_update_task_state_invalid_id(conn):
    # zkusíme aktualizovat stav neexistujícího úkolu
    non_existent_task_id = 99999
    with pytest.raises(ValueError) as error:
        update_task_state(conn, non_existent_task_id, "completed")
    assert (
        str(error.value) == "Invalid task ID."
    ), f"Očekáváme chybovou hlášku 'Invalid task ID.', ale dostali jsme {str(error.value)}"


@pytest.mark.testDeleteTask
def test_delete_task_ok(conn):
    # přidáme úkol ve stavu čekající
    add_task(conn, "Úkol určený ke smazání", "Nějaký popis úkolu", "pending")

    # získat ID přidaného úkolu
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        f"SELECT id FROM tasks WHERE name = %s AND description = %s AND state = %s",
        ("Úkol určený ke smazání", "Nějaký popis úkolu", "pending"),
    )
    task = cursor.fetchone()
    task_id = task["id"]

    # odstraň úkol
    delete_task(conn, task_id)

    # ověř, že se úkolu smazal
    cursor.execute(f"SELECT state FROM tasks WHERE id = %s", (task_id,))
    deleted_task = cursor.fetchone()

    assert (
        deleted_task == None
    ), f"Očekáváme, že smazaný úkol nebude v databázi, ale je stále tam je."


@pytest.mark.testDeleteTask
def test_delete_task_fail(conn):
    # odstraň neexistující úkol

    with pytest.raises(ValueError) as error:
        delete_task(conn, 9999)
    assert (
        str(error.value) == "Invalid task ID."
    ), f"Očekáváme chybovou hlášku 'Invalid task ID.', ale dostali jsme {str(error.value)}"
