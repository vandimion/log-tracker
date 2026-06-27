import sqlite3
from datetime import datetime, timedelta

def connect(db_path):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row # access columns by name
    return conn

def get_db_info(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM employees")
    employee_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM login_logs")
    log_count = cursor.fetchone()[0]
    return{
        "employee_count": employee_count,
        "log_count": log_count
    }

def flag_failed_logins(conn, threshold = 5):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            e.full_name,
            e.email,
            d.name as department,
            COUNT(*) as failure_count
        FROM login_logs l
        JOIN employees e ON l.employee_id = e.id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE l.status = 'failure'
        GROUP BY l.employee_id
        HAVING COUNT(*) > ?
        ORDER BY failure_count DESC
    """, (threshold,))
    return cursor.fetchall()

def flag_off_hours(conn, start_hour = 9, end_hour = 17):
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            e.full_name,
            e.email,
            d.name as department,
            COUNT(*) as off_hours_count,
            MIN(l.timestamp) as first_occurrence,
            MAX(l.timestamp) as last_occurrence
        FROM login_logs l
        JOIN employees e ON l.employee_id = e.id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE CAST(strftime('%H', l.timestamp) AS INTEGER) < ?
           OR CAST(strftime('%H', l.timestamp) AS INTEGER) >= ?
        GROUP BY l.employee_id
        ORDER BY off_hours_count DESC
    """, (start_hour, end_hour))
    return cursor.fetchall()

def flag_inactive(conn, days = 30):
    cursor = conn.cursor()
    cutoff = (datetime.now() - timedelta(days = days)).strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        SELECT
            e.full_name,
            e.email,
            MAX(l.timestamp) as last_login,
            d.name as department
        FROM employees e
        LEFT JOIN login_logs l ON e.id = l.employee_id
        LEFT JOIN departments d ON e.department_id = d.id
        WHERE e.is_active = 1
        GROUP BY e.id
        HAVING last_login IS NULL OR last_login < ?
        ORDER BY last_login ASC
    """, (cutoff,))
    return cursor.fetchall()

def analyze(db_path, threshold = 5, start_hour = 9, end_hour = 17, inactive_days = 30):
    conn = connect(db_path)

    results = {
        "db_path":          db_path,
        "failed_logins":    flag_failed_logins(conn, threshold),
        "off_hours":        flag_off_hours(conn, start_hour, end_hour),
        "inactive":         flag_inactive(conn, inactive_days),
        "info":             get_db_info(conn)
    }

    conn.close()
    return results

# checker for db needed
if __name__ == "__main__":
    results = analyze("data/test-database.db")
    
    print(f"--- Database Name: {results['db_path']}")
    print(f"--- Employee Count: {results['info']['employee_count']}")
    print(f"--- Total Logs: {results['info']['log_count']}")

    print("\n--- Failed Logins ---")
    for row in results["failed_logins"]:
        print(f"  {row['full_name']} ({row['email']}) — {row['failure_count']} failures")
    
    print("\n--- Off Hours ---")
    for row in results["off_hours"]:
        print(f"  {row['full_name']} ({row['email']}) — {row['off_hours_count']} logins")
    
    print("\n--- Inactive Accounts ---")
    for row in results["inactive"]:
        print(f"  {row['full_name']} ({row['email']}) — last login: {row['last_login']}")