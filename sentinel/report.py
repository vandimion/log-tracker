# to-do:
# add rich platform for better printing of results

from datetime import datetime

def print_header(results):
    print("\nLOG INSPECTOR")
    print(f"Database    :   {results['db_path']}")
    print(f"Employees   :   {results['info']['employee_count']}")
    print(f"Total Logs  :   {results['info']['log_count']}")
    print(f"Run         :   {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 40)

def print_failed_logins(rows):
    print("\nFailed Logins")
    if not rows:
        print("No accounts flagged.")
        return
    for row in rows:
        print(f"    {row['full_name']} ({row['email']}) — {row['failure_count']} failures")

def print_off_hours(rows):
    print("\nOff-Hours Logins")
    if not rows:
        print("No accounts flagged.")
        return
    for row in rows:
        print(f"    {row['full_name']} ({row['email']}) — {row['off_hours_count']} logins")

def print_inactive(rows):
    print("\nInactive Accounts")
    if not rows:
        print("No accounts flagged.")
        return
    for row in rows:
        print(f"    {row['full_name']} ({row['email']}) — last login: {row['last_login'] or 'Never'}")

def print_report(results):
    print_header(results)
    print_failed_logins(results["failed_logins"])
    print_off_hours(results["off_hours"])
    print_inactive(results["inactive"])
    print("\nReport complete.")

if __name__ == "__main__":
    from analyzer import analyze
    results = analyze("data/test-database.db")
    print_report(results)
