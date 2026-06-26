import sqlite3
import os
import random
from faker import Faker
from datetime import datetime, timedelta
fake = Faker()

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
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                full_name       TEXT NOT NULL,
                email           TEXT NOT NULL UNIQUE,
                department_id   INTEGER REFERENCES departments(id),
                is_active       INTEGER DEFAULT 1,
                created_at      TEXT DEFAULT CURRENT_TIMESTAMP
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

def seed_data(conn, config):
    cursor = conn.cursor()

    # departments
    dept_ids = []
    if "departments" in config["tables"]:
        for dept in config["departments"]:
            cursor.execute(
                "INSERT OR IGNORE INTO departments (name) VALUES (?)",
                (dept,)
            )
        conn.commit()

        # fetch back ids
        cursor.execute("SELECT id FROM departments")
        dept_ids = [row[0] for row in cursor.fetchall()]
        print(f"Inserted {len(dept_ids)} departments.")

    # employees (fake IDs)
    employee_ids = []
    if "employees" in config["tables"]:
        for _ in range(config["num_employees"]):
            full_name = fake.name()
            email     = fake.unique.email()
            dept_id   = random.choice(dept_ids) if dept_ids else None
            
            cursor.execute(
                """INSERT INTO employees (full_name, email, department_id, is_active) 
                    VALUES (?, ?, ?, 1)""",
                (full_name, email, dept_id)
            )
        
        conn.commit()

        cursor.execute("SELECT id FROM employees")
        employee_ids = [row[0] for row in cursor.fetchall()]
        print(f"Inserted {len(employee_ids)} employees.")

    # login logs
    if "login_logs" in config["tables"]:
        end   = datetime.now()
        start = end - timedelta(days = config["history_days"])

        burst_count   = {"low":1, "medium":2, "high": 4}[config["anomaly_level"]]
        offhour_count = {"low":1, "medium":2, "high": 3}[config["anomaly_level"]]
        dormant_count = {"low":1, "medium":2, "high": 3}[config["anomaly_level"]]

        burst_users   = random.sample(employee_ids, min(burst_count, len(employee_ids)))
        offhour_users = random.sample(employee_ids, min(offhour_count, len(employee_ids)))
        dormant_users = random.sample(
            [e for e in employee_ids if e not in burst_users],
            min(dormant_count, len(employee_ids) - len(burst_users))
        )

        for emp_id in employee_ids:
            # dormant users get old logins
            if emp_id in dormant_users:
                old_end = end - timedelta(days = 30)
                for _ in range(random.randint(1, 3)):
                    ts = start + timedelta(
                        seconds = random.randint(0, int((old_end - start).total_seconds()))
                    )
                    cursor.execute(
                        "INSERT INTO login_logs (employee_id, timestamp, status, ip_address) VALUES (?, ?, ?, ?)",
                        (emp_id, ts.strftime("%Y-%m-%d %H:%M:%S"), "success", f"192.168.1.{random.randint(1, 50)}")
                    )
                continue

            for _ in range(random.randint(3, 10)):
                ts = start + timedelta(
                    seconds = random.randint(0, int((end - start).total_seconds()))
                )
                status = random.choices(["success", "failure"], weights = [90, 10])[0]
                cursor.execute(
                    "INSERT INTO login_logs (employee_id, timestamp, status, ip_address) VALUES (?, ?, ?, ?)",
                    (emp_id, ts.strftime("%Y-%m-%d %H:%M:%S"), status, f"192.168.1.{random.randint(1, 50)}")
                )

                if emp_id in burst_users:
                    burst_start = end - timedelta(hours = random.randint(2, 48))
                    for _ in range(random.randint(8, 15)):
                        ts = burst_start + timedelta(minutes = random.randint(1, 60))
                        cursor.execute(
                            "INSERT INTO login_logs (employee_id, timestamp, status, ip_address) VALUES (?, ?, ?, ?)",
                            (emp_id, ts.strftime("%Y-%m-%d %H:%M:%S"), "failure", f"10.0.0.{random.randint(1,50)}")
                        )

                if emp_id in offhour_users:
                    for _ in range(random.randint(2, 5)):
                        ts = start + timedelta(
                            seconds = random.randint(0, int((end - start).total_seconds()))
                        )
                        ts = ts.replace(hour = random.choice([1, 2, 3, 22, 23]))
                        cursor.execute(
                            "INSERT INTO login_logs (employee_id, timestamp, status, ip_address) VALUES (?, ?, ?, ?)",
                            (emp_id, ts.strftime("%Y-%m-%d %H:%M:%S"), "success", f"203.0.113.{random.randint(1,50)}")
                        )
            
            conn.commit()
            
        print(f"Login logs inserted.")

def build_database(config):
    print("\nBuilding database...")
    conn = connect_db(config)
    create_tables(conn, config["tables"])
    seed_data(conn, config)
    conn.close()
    print(f"\nDone. Database '{config['db_name']}.db' saved in data/")

if __name__ == "__main__":
    print("Run admin/wizard.py to create a database.")