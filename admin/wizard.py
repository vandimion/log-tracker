# to add:
# reprompt if question - proceed with these settings - is "no"

import questionary
import sys
from builder import build_database
import time

def ask_number(prompt, default):
    answer = questionary.text(prompt, default = default).ask()
    while not answer.strip() or not answer.strip().isdigit():
        print("Please enter a valid number.")
        answer = questionary.text(prompt, default = default).ask()
    return int(answer)

def ask_departments():
    print("Enter each department separated by a comma.")
    time.sleep(1.25)
    print("Example: HR, IT, Finance, Operations")
    time.sleep(1.25)
    dept_input = questionary.text(
        "Enter department names (comma separated):",
    ).ask()
    departments = [d.strip() for d in dept_input.split(",") if d.strip()]
    while not departments:
        print("Please enter at least one department")
        print("Example: HR, IT, Finance")
        time.sleep(1)
        dept_input = questionary.text(
            "Enter department names (comma separated):"
        ).ask()
        departments = [d.strip() for d in dept_input.split(",") if d.strip()]
    return departments

def confirm_summary(config):
    print("\nDatabase Details")
    for key, value in config.items():
        print(f"    {key}:  {value}")
    proceed = questionary.confirm(
        "\nProceed with these settings?",
        default = True
    ).ask()
    if not proceed:
        print("Cancelled. No database created.")
        return False
    return True

def run_wizard(): # create config dict
    try:
        print("\nDATABASE CREATION")
        print("Press Ctrl key + C to cancel anytime.")

        if not questionary.confirm("Create new database", default = True).ask():
            print("No database created. Exiting program...")
            return None

        db_name = questionary.text("Name of database:", default="").ask()
        while not db_name.strip() or len(db_name) > 45:
            if not db_name.strip():
                print("Database name cannot be empty.")
            else:
                print("Database name cannot exceed 50 characters.")
            db_name = questionary.text("Name of database:").ask()

        reset = questionary.confirm(
            "Reset if already exists?", default = False
        ).ask()

        departments = ask_departments()
        num_employees = ask_number("How many employees?", "20")
        history_days = ask_number("How many days of login history?", "30")

        anomaly_level = questionary.select(
            "Anomaly level?",
            choices = ["low", "medium", "high"],
        ).ask()

        config = {
            "db_name":       db_name,
            "reset":         reset,
            "tables":        ["employees", "departments", "login_logs"],
            "departments":   departments,
            "num_employees": num_employees,
            "history_days":  history_days,
            "anomaly_level": anomaly_level,
        }

        if not confirm_summary(config):
            return None

        return config
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    config = run_wizard()
    if config:
        build_database(config) # To comment out when testing
        
        # Test code
        
        # print("\nTest")
        # for key, value in config.items():
        #     print(f"   {key}:  {value}")