# create database
# # to do:
# function to reset database if it exists
# simplify functions
# allow user to change output

import questionary
import sys

def run_wizard(): # ask and return config dict
    
    try:
        print("\nDATABASE CREATION")
        print("Press Ctrl + C to cancel program anytime.")
        create = questionary.confirm("Create new database?", default=True).ask()

        if not create:
            print("No database created. Exiting program...")
            return None

        # database name
        db_name = questionary.text(
            "Name of database: ",
            default = ""
        ).ask()

        while not db_name.strip():
            print("Database name cannot be empty.")
            db_name = questionary.text("Name of database: ").ask()

        reset = questionary.confirm(
            "Reset the database if it already exists?",
            default = False
        ).ask()

        # table name/s
        tables = questionary.checkbox(
            "Which tables to create?",
            choices = ["employees", "departments", "login_logs"]
        ).ask()

        while not tables:
            print("Please select at least one table.")
            tables = questionary.checkbox(
                "Which tables to create?",
                choices = ["employees", "departments", "login_logs"]
            ).ask()

        # employee count
        num_employees = questionary.text(
            "How many employees?",
        ).ask()

        while not num_employees.strip() or not num_employees.replace(" ","").isdigit():
            print("Please enter a valid number.")
            num_employees = questionary.text("How many employees?").ask()

        history_days = questionary.text(
            "How many days of login history?",
        ).ask()

        while not history_days.strip() or not history_days.replace(" ","").isdigit():
            print("Please enter a valid number.")
            history_days = questionary.text("How many days of login history?").ask()

        anomaly_level = questionary.select(
            "Anomaly level?",
            choices = ["low", "medium", "high"],
        ).ask()

        config = {
            "db_name": db_name,
            "reset": reset,
            "tables": tables,
            "num_employees": int(num_employees),
            "history_days": int(history_days),
            "anomaly_level": anomaly_level
        }
        return config
        
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user. Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    config = run_wizard()
    if config:
        print("\nDatabase Details")
        for key, value in config.items():
            print(f"{key}:{value}")

print("\nAre you sure these details are correct?")

# add validator function after