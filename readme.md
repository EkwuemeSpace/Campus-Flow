# CampusFlow — Helpdesk Ticket Management System

CampusFlow is a Python command-line helpdesk application designed to help campus IT support teams create, prioritize, assign, track, and manage support tickets efficiently.

The project demonstrates practical software engineering concepts, including modular design, input validation, ticket workflow management, JSON file persistence, and automated unit testing.

## Features

- **Ticket Management:** Create, list, and view support tickets.
- **Automatic Prioritization:** Assign priorities based on urgency and the number of affected users.
- **Ticket Assignment:** Assign unassigned tickets to support staff.
- **Workflow Management:** Track tickets through `open`, `in_progress`, and `resolved` statuses.
- **Persistent Storage:** Save tickets to a JSON file and reload them when the application starts.
- **Unresolved Ticket Queue:** Sort unresolved tickets by priority, then by ticket ID.
- **Reports:** View total tickets and breakdowns by status and priority.
- **Input Validation:** Reject invalid ticket information and unsupported workflow transitions.
- **Automated Testing:** Use Python's built-in `unittest` framework to verify application behavior.

## Technology Stack

- Python
- JSON
- `pathlib`
- `unittest`

No third-party Python packages are required for the application's core functionality.

## Getting Started

### Prerequisites

- Python 3.10 or later recommended.
- Git, if you want to clone the repository.

### Installation

Clone the repository and enter the project directory:

```bash
git clone <your-repository-url>
cd "Campus Flow"
```

Create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**Linux/macOS:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Run the application

```bash
python main.py
```

Follow the interactive menu to create, view, assign, and update tickets.

### Run the tests

```bash
python -m unittest discover -s tests -v
```

## Ticket Prioritization Rules

CampusFlow calculates priority using urgency and the number of affected users.

| Condition | Priority |
|---|---|
| High urgency and at least 10 affected users | Critical |
| High urgency or at least 10 affected users | High |
| Medium urgency or at least 3 affected users | Medium |
| All other valid cases | Low |

The rules are evaluated from highest to lowest priority.

## Ticket Workflow

Tickets follow a controlled workflow:

- `open`: A ticket has been created.
- `in_progress`: Work has started; the ticket must be assigned first.
- `resolved`: The issue has been resolved.

A resolved ticket must be explicitly reopened before it can move through the workflow again.

## Project Structure

```text
Campus Flow/
├── campusflow/
│   ├── __init__.py
│   ├── tickets.py
│   ├── workflow.py
│   └── storage.py
├── tests/
│   ├── test_tickets.py
│   └── test_storage.py
├── docs/
│   ├── requirements.md
│   └── design-decisions.md
├── data/
├── main.py
├── .gitignore
└── README.md
```

The `data/` directory and `tickets.json` file are created when ticket data is saved.

## Learning Objectives

This project provides practical experience with:

- Breaking a problem into smaller modules.
- Designing functions with clear responsibilities.
- Validating user input and handling errors.
- Managing application state and JSON persistence.
- Enforcing business rules and workflow transitions.
- Writing automated tests with `unittest`.
- Using Git and GitHub to document software development.

## Current Status

CampusFlow is under active development. Core ticket management, workflow, and JSON storage modules have been implemented and tested. The command-line interface integrates these modules.

## Future Improvements

Potential extensions include:

- Search and filtering.
- Ticket editing and deletion.
- Staff accounts and role-based permissions.
- A graphical or web-based interface.
- Database-backed storage.

## License

No license has been selected yet. Until a license is added, reuse and redistribution are not automatically permitted.
