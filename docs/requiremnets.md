# CampusFlow — Requirements

## Project Goal
Build a Python command-line helpdesk application that manages campus technical support tickets.

## Core Features
1. Create tickets with validated inputs.
2. Automatically generate unique ticket IDs.
3. Calculate ticket priority using predefined rules.
4. List all tickets and view individual tickets.
5. Assign tickets to staff.
6. Manage ticket status and reopening.
7. Display an ordered work queue.
8. Generate ticket reports.
9. Save and reload tickets using JSON.

## Validation Rules
- Ticket title cannot be blank.
- Category must be Network, Hardware, Software, or Other.
- Urgency must be low, medium, or high.
- Affected users must be a positive integer.
- Unknown ticket IDs and invalid status transitions must be rejected.

## Technical Requirements
- Language: Python
- Interface: Command-line interface (CLI)
- Storage: JSON
- Testing: unittest
- Minimum: 8 meaningful automated tests

## Completion Criteria
All required features work, invalid operations are handled safely, saved tickets survive application restarts, and the automated tests pass.