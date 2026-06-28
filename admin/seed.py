# quick hardcoded seed for development and testing

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from admin.builder import build_database

# ── Hardcoded config ──────────────────────────────────────────────────────────

SEED_CONFIG = {
    "db_name":       "test_database",
    "reset":         True,
    "tables":        ["employees", "departments", "login_logs"],
    "departments":   [
        "Human Resources",
        "Information Technology",
        "Finance",
        "Operations",
        "Legal",
        "Marketing",
    ],
    "num_employees": 20,
    "history_days":  60,
    "anomaly_level": "medium",
}

# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("SEED SCRIPT")
    print("-" * 40)
    print(f"  Database    : {SEED_CONFIG['db_name']}.db")
    print(f"  Employees   : {SEED_CONFIG['num_employees']}")
    print(f"  History     : {SEED_CONFIG['history_days']} days")
    print(f"  Anomalies   : {SEED_CONFIG['anomaly_level']}")
    print(f"  Departments : {', '.join(SEED_CONFIG['departments'])}")
    print("-" * 40)

    confirm = input("\nCreate database? (Y/n): ").strip().lower()
    if confirm == "n":
        print("Cancelled.")
        sys.exit(0)

    build_database(SEED_CONFIG)
    print("\nSeed complete. Run the analyzer with:")
    print(f"  python sentinel/cli.py --db data/{SEED_CONFIG['db_name']}.db")