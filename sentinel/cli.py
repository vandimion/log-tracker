import argparse
import os
import sys
from analyzer import analyze
from report import print_report

def list_databases():
    """Find all .db files in data/ folder."""
    if not os.path.exists("data"):
        return[]
    return [f for f in os.listdir("data") if f.endswith(".db")]

def ask_database():
    """Interactively prompt user to select a database."""
    databases = list_databases()

    if not databases:
        print("No databases found in data/ directory.")
        print(" Run python admin/wizard.py first to generate one.")
        sys.exit(1)

    print("\nAvailable databases:")
    for i, db in enumerate(databases, 1):
        print(f"  [{i}] {db}")

    print("\nEnter number to select or type a custom path:")
    choice = input("> ").strip()

    if choice.isdigit():
        index = int(choice) - 1
        if 0 <= index < len(databases):
            return f"data/{databases[index]}"
        else:
            print("Invalid selection.")
            sys.exit(1)
    elif os.path.exists(choice):
        return choice
    else:
        print(f"Error: '{choice}' not found.")
        sys.exit(1)

def ask_int(prompt, default, min_val=1, max_val=999):
    while True:
        value = input(f"{prompt} [{default}]: ").strip()
        if not value:
            return default
        if value.isdigit() and min_val <= int(value) <= max_val:
            return int(value)
        print(f"  Please enter a number between {min_val} and {max_val}.")

def ask_hours():
    while True:
        start = ask_int("Business hours start (24-hour format)", 9, min_val=0, max_val=23)
        end   = ask_int("Business hours end (24-hour format)",  17, min_val=0, max_val=23)
        if start < end:
            return start, end
        print("  Start hour must be less than end hour. Try again.")

def interactive_mode():
    print("\nLOG INSPECTOR")
    print("-" * 40)
    print("Press Enter to use default values.\n")

    db_path       = ask_database()
    threshold     = ask_int("Failed login threshold",  5,  min_val=1, max_val=999)
    start_hour, end_hour = ask_hours()
    inactive_days = ask_int("Inactive days threshold", 30, min_val=1, max_val=365)

    print(f"\n  Database      : {db_path}")
    print(f"  Threshold     : {threshold}")
    print(f"  Business hours: {start_hour}:00 - {end_hour}:00")
    print(f"  Inactive days : {inactive_days}")

    confirm = input("\nProceed? (Y/n): ").strip().lower()
    if confirm == "n":
        print("Cancelled.")
        sys.exit(0)

    return db_path, threshold, start_hour, end_hour, inactive_days

def build_parser():
    parser = argparse.ArgumentParser(
        prog="log-inspector",
        description="Analyze employee login logs and flag suspicious activity.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sentinel/cli.py                                  (interactive)
  python sentinel/cli.py --db data/log_inspector.db
  python sentinel/cli.py --threshold 3 --inactive-days 45
  """
    )
    parser.add_argument("--db",            default=None,  metavar="PATH", help="Path to database file")
    parser.add_argument("--threshold",     default=None,  metavar="N",    help="Failed login threshold (default: 5)",    type=int)
    parser.add_argument("--start-hour",    default=None,  metavar="H",    help="Business hours start (default: 9)",      type=int)
    parser.add_argument("--end-hour",      default=None,  metavar="H",    help="Business hours end (default: 17)",       type=int)
    parser.add_argument("--inactive-days", default=None,  metavar="N",    help="Inactive days threshold (default: 30)",  type=int)
    parser.add_argument("--version",       action="version", version="log-inspector 1.0.0")
    return parser

def validate_args(db, threshold, start_hour, end_hour, inactive_days):
    if not os.path.exists(db):
        print(f"Error: Database not found at '{db}'")
        print("Run python admin/wizard.py first.")
        sys.exit(1)
    if threshold < 1:
        print("Error: threshold must be at least 1.")
        sys.exit(1)
    if not 0 <= start_hour < end_hour <= 23:
        print(f"Error: invalid hours. start ({start_hour}) must be less than end ({end_hour}).")
        sys.exit(1)
    if inactive_days < 1:
        print("Error: inactive-days must be at least 1.")
        sys.exit(1)

def main():
    parser = build_parser()
    args = parser.parse_args()

    # if no arguments passed, launch interactive mode
    if args.db is None:
        db, threshold, start_hour, end_hour, inactive_days = interactive_mode()
    else:
        db            = args.db
        threshold     = args.threshold     or 5
        start_hour    = args.start_hour    or 9
        end_hour      = args.end_hour      or 17
        inactive_days = args.inactive_days or 30

    validate_args(db, threshold, start_hour, end_hour, inactive_days)

    print("\nRunning analysis...")
    results = analyze(
        db_path=db,
        threshold=threshold,
        start_hour=start_hour,
        end_hour=end_hour,
        inactive_days=inactive_days
    )
    print_report(results)

if __name__ == "__main__":
    main()