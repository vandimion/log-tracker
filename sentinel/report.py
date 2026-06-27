from rich.console import Console
from rich.table import Table
from rich import box
from datetime import datetime

console = Console()

def print_header(results):
    console.print("\n[bold cyan]LOG INSPECTOR[/bold cyan]", justify="center")
    console.print(f"[dim]Database: {results['db_path']}[/dim]", justify="center")
    console.print(f"[dim]Employees: {results['info']['employee_count']} | "
                  f"Total Logs: {results['info']['log_count']} | "
                  f"Time Executed : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n",
                  justify="center")

def print_failed_logins(rows):
    console.print("[bold red]Failed Logins[/bold red]")
    if not rows:
        console.print("  [green]No accounts flagged.[/green]\n")
        return
    table = Table(box=box.SIMPLE)
    table.add_column("Name",          style="white")
    table.add_column("Email",         style="dim")
    table.add_column("Department",    style="cyan")
    table.add_column("Failures",      style="red",  justify="right")
    for row in rows:
        table.add_row(
            row["full_name"], 
            row["email"], 
            row["department"] or "N/A",
            str(row["failure_count"]))
    console.print(table)

def print_off_hours(rows):
    console.print("[bold yellow]Off-Hours Logins[/bold yellow]")
    if not rows:
        console.print("  [green]No accounts flagged.[/green]\n")
        return
    table = Table(box=box.SIMPLE)
    table.add_column("Name",                    style="white")
    table.add_column("Email",                   style="dim")
    table.add_column("Department",              style="cyan")
    table.add_column("Count",                   style="yellow", justify="right")
    table.add_column("First Off-Hours Login",   style="dim")
    table.add_column("Last Off-Hours Login",    style="dim")
    for row in rows:
        table.add_row(
            row["full_name"],
            row["email"],
            row["department"] or "N/A",
            str(row["off_hours_count"]),
            row["first_occurrence"],
            row["last_occurrence"]
        )
    console.print(table)

def print_inactive(rows):
    console.print("[bold magenta]Inactive Accounts[/bold magenta]")
    if not rows:
        console.print("  [green]No accounts flagged.[/green]\n")
        return
    table = Table(box=box.SIMPLE)
    table.add_column("Name",        style="white")
    table.add_column("Email",       style="dim")
    table.add_column("Department",  style="cyan")
    table.add_column("Last Login",  style="magenta")
    for row in rows:
        table.add_row(
            row["full_name"],
            row["email"],
            row["department"] or "N/A",
            row["last_login"] or "Never"
        )
    console.print(table)

def print_report(results):
    print_header(results)
    print_failed_logins(results["failed_logins"])
    print_off_hours(results["off_hours"])
    print_inactive(results["inactive"])
    console.print("[dim]Report complete.[/dim]\n")

if __name__ == "__main__":
    from analyzer import analyze
    results = analyze("data/test-database.db")
    print_report(results)
