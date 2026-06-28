# log-inspector

A command-line tool that analyzes employee login logs and flags suspicious activity.

Built with Python and SQLite.

---

## What It Detects

- Failed logins above a set threshold
- Logins outside business hours
- Accounts with no recent activity

---

## Requirements

- Python 3.11+
- pip

---

## Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/YOUR_USERNAME/log-inspector.git
cd log-inspector
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:** All required packages are listed in `requirements.txt`. 
> If you add new packages during development always run:
> `pip freeze > requirements.txt`

## How to Use

### Step 1 — Generate a database (Admin)

Run the wizard to create and seed a database interactively:

```bash
python admin/wizard.py
```

Or use the quick seed script for testing:

```bash
python admin/seed.py
```

### Step 2 — Run the analyzer (Client)

Interactive mode:

```bash
python sentinel/cli.py
```

Direct mode:

```bash
python sentinel/cli.py --db data/log_inspector.db
python sentinel/cli.py --db data/log_inspector.db --threshold 3
python sentinel/cli.py --db data/log_inspector.db --start-hour 8 --end-hour 18
python sentinel/cli.py --db data/log_inspector.db --inactive-days 45
```

---

## Options

| Flag | Default | Description |
|---|---|---|
| `--db` | data/log_inspector.db | Path to database |
| `--threshold` | 5 | Failed logins before flagging |
| `--start-hour` | 9 | Business hours start |
| `--end-hour` | 17 | Business hours end |
| `--inactive-days` | 30 | Days before account flagged inactive |

---

## Project Structure

```
log-inspector/
│
├── admin/
│   ├── wizard.py       # interactive database setup
│   ├── builder.py      # schema creation and data seeding
│   └── seed.py         # quick hardcoded seed for testing
│
├── sentinel/
│   ├── analyzer.py     # SQL queries and detection logic
│   ├── report.py       # terminal output formatting
│   └── cli.py          # command-line entrypoint
│
├── data/               # directory for generated databases 
│
├── .gitignore
├── requirements.txt    # tools to be installed during setup
└── README.md
```

## Tech Stack

- Python 3.11
- SQLite via sqlite3
- questionary — interactive CLI prompts
- faker — realistic mock data generation
- rich — formatted terminal output
