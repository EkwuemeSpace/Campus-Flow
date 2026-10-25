# CampusFlow — Design Decisions

## 1. Programming Language
Python.

## 2. Ticket Data Structure
Each ticket will be represented as a Python dictionary. Tickets will be held in a collection while the application runs.

## 3. Module Responsibilities
- `tickets.py`: Ticket creation, input validation, ID generation, and priority calculation.
- `workflow.py`: Ticket assignment, status transitions, and work queue.
- `storage.py`: Saving and loading tickets from JSON.
- `reports.py`: Ticket statistics and reports.
- `main.py`: CLI menu and user interaction.

## 4. Error Handling
Functions will reject invalid operations with clear exceptions. The CLI will display helpful error messages.

## 5. Testing
Business logic will be tested independently using Python's `unittest` module.

## 6. Persistence
Tickets will be saved in JSON and reloaded when the application starts.

## 7. Development Approach
Build and test each module separately before integrating everything through the CLI.
