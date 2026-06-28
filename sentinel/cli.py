import argparse
import os
import sys
from analyzer import analyze
from report import print_report

def main():
    parser = argparse.ArgumentParser(
        prog="log-inspector",
        description="Analyze employee login logs and flag suspicious activity."
    )
    parser.add_argument("--db",            default="data/.db")
    parser.add_argument("--threshold",     type=int, default=5)
    parser.add_argument("--start-hour",    type=int, default=9)
    parser.add_argument("--end-hour",      type=int, default=17)
    parser.add_argument("--inactive-days", type=int, default=30)
    args = parser.parse_args()

    if not os.path.exists(args.db):
        print(f"Error: Database not found at '{args.db}'")
        print("Run python admin/wizard.py first.")
        sys.exit(1)

    results = analyze(
        db_path=args.db,
        threshold=args.threshold,
        start_hour=args.start_hour,
        end_hour=args.end_hour,
        inactive_days=args.inactive_days
    )
    print_report(results)

if __name__ == "__main__":
    main()