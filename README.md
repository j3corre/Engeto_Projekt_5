# Task Manager s MySQL databází

Jednoduchá konzolová aplikace pro správu úkolů s využitím MySQL databáze. Aplikace umožňuje přidávat, zobrazovat, aktualizovat a mazat úkoly (CRUD operace).

## Požadavky

- Python 3.10 nebo novější
- MySQL server
- Virtuální prostředí (venv)

## Instalace a nastavení

1. Vytvořte a aktivujte virtuální prostředí:

```bash
# Vytvoření virtuálního prostředí
python -m venv engetop5

# Aktivace na Windows
engetop5\Scripts\activate

# Aktivace na macOS/Linux
source engetop5/bin/activate
```

2. Nainstalujte potřebné knihovny:

```bash
pip install mysql-connector-python python-dotenv
```

3. Vytvořte soubor `.env` v kořenovém adresáři projektu s následující konfigurací:

```env
DB_HOST=localhost
DB_USER=vas_uzivatel
DB_PASSWORD=vase_heslo
DB_NAME=task_manager
```

## Struktura projektu

```
├── main.py                 # Hlavní spouštěcí soubor
├── src/
│   └── task_manager_db.py # Modul pro práci s databází
├── .env                   # Konfigurační soubor (nutno vytvořit)
└── README.md             
```

## Modul task_manager_db.py

Modul poskytuje následující funkce pro práci s databází:

### Hlavní funkce

- `connect_to_database(host, user, password, database)` 
  - Vytvoří připojení k MySQL databázi
  - Vrací objekt připojení

- `initialize_database(host, user, password, db_name)`
  - Inicializuje databázi a vytvoří tabulku úkolů
  - Vytvoří databázi a tabulku, pokud neexistují

- `add_task(connection, name, description, state)`
  - Přidá nový úkol do databáze
  - Parametr state může být: 'pending', 'in_progress', 'completed'

- `get_tasks(connection)`
  - Vrátí seznam všech úkolů
  - Úkoly jsou seřazeny podle času vytvoření

- `update_task_state(connection, task_id, new_state)`
  - Aktualizuje stav úkolu
  - Možné stavy: 'pending', 'in_progress', 'completed'

- `delete_task(connection, task_id)`
  - Odstraní úkol z databáze

- `close_connection(connection)`
  - Bezpečně uzavře připojení k databázi

### Struktura databáze

Tabulka `tasks` obsahuje následující sloupce:
- `id` (INT, AUTO_INCREMENT, PRIMARY KEY)
- `name` (VARCHAR(100))
- `description` (VARCHAR(255))
- `state` (ENUM: 'pending', 'in_progress', 'completed')
- `created_at` (TIMESTAMP)

## Spuštění aplikace

1. Ujistěte se, že máte spuštěný MySQL server
2. Zkontrolujte, že máte správně nastavený soubor `.env`
3. Aktivujte virtuální prostředí
4. Spusťte aplikaci příkazem:

```bash
python main.py
```

## Funkcionalita aplikace

Po spuštění aplikace se zobrazí hlavní menu s následujícími možnostmi:

1. **Přidat nový úkol**
   - Umožňuje vytvořit nový úkol
   - Vyžaduje zadání názvu (max. 100 znaků) a popisu (max. 255 znaků)
   - Nový úkol je automaticky vytvořen ve stavu "nezahájeno"

2. **Zobrazit úkoly**
   - Zobrazí seznam všech úkolů
   - U každého úkolu je vidět název, popis, stav a datum vytvoření
   - Úkoly jsou řazeny podle data vytvoření

3. **Aktualizovat úkol**
   - Umožňuje změnit stav existujícího úkolu
   - Nabízí změnu stavu na:
     - Probíhá (in_progress)
     - Hotovo (completed)

4. **Odstranit úkol**
   - Umožňuje odstranit vybraný úkol ze seznamu
   - Před odstraněním zobrazí seznam úkolů k výběru

5. **Ukončit program**
   - Bezpečně ukončí aplikaci
   - Uzavře připojení k databázi

### Perzistence dat

Důležitou vlastností aplikace je, že všechny úkoly jsou ukládány do MySQL databáze. To znamená, že:
- Data zůstávají zachována i po ukončení programu
- K úkolům lze přistupovat z různých spuštění aplikace
- Data jsou bezpečně uložena v databázi a nejsou závislá na běhu programu
- Při novém spuštění programu jsou dostupné všechny dříve vytvořené úkoly

## Poznámky k vývoji

- Aplikace používá knihovnu `python-dotenv` pro bezpečnou správu konfigurace
- Připojení k databázi je automaticky uzavíráno po každé operaci
- Chybové stavy jsou ošetřeny pomocí vlastních výjimek
- Kód obsahuje kompletní dokumentaci funkcí pomocí docstringů

## Poznámky k automatickým testům

- Připraveno je celkem 19 testů pro `pytest`. Jsou jak pozitivní, tak negativní, a testují funkce `add_task()`, `get_tasks()`, `update_task_state()` a `delete_task()`
- Lze je spustit všechny najednou, nebo je lze spouštět jednotlivě pro testované funkce pomocí
```bash
pytest -m testAddTask
pytest -m testgetTasks
pytest -m testUpdateTaskState
pytest -m testDeleteTask
```

## Autor

Jan Bláha (jan.blaha@bcas.cz)

## Licence

Tento projekt je volně k použití a modifikaci.