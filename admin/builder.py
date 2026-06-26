import sqlite3
import os

def connect_db(config):
    db_path = f"data/{config['db_name']}.db"

    # if reset is true
    if config["reset"] and os.path.exists(db_path):
        os.remove(db_path)
        print(f"Existing database removed.")

    conn = sqlite3.connect(db_path)
    print(f"Connected to {db_path}")
    return conn

def create_tables(conn, tables):
    cursor = conn.cursor()

    if "departments" in tables:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS departments (
                id   INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE
            )
        """)
        print("Created table: departments")

    if "employees" in tables:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS employees (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name   TEXT NOT NULL,
                email       TEXT NOT NULL UNIQUE,
                dept_id     INTEGER REFERENCES departments(id),
                is_active   INTEGER DEFAULT 1,
                created_at  TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("Created table: employees")

    if "login_logs" in tables:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS login_logs (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER REFERENCES employees(id),
                timestamp   TEXT NOT NULL,
                status      TEXT NOT NULL,
                ip_address  TEXT NOT NULL
            )
        """)
        print("Created table: login_logs")
    
    conn.commit()

if __name__ == "__main__":
    test_config = {
        "db_name": "test_db",
        "reset": True,
        "tables": ["employees", "departments", "login_logs"],
        "departments": [],
        "num_employees": 5,
        "history_days": 10,
        "anomaly_level": "low"
    }
    conn = connect_db(test_config)
    create_tables(conn, test_config["tables"])
    conn.close()
    print("Test successful.")