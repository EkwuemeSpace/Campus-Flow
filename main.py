
# Import the existing ticket, workflow, and storage functions.
from campusflow.tickets import (
    create_ticket,
    add_ticket,
    get_ticket,
    list_tickets,
    assign_ticket,
)
from campusflow.workflow import update_status
from campusflow.storage import load_tickets, save_tickets


# Define the application's data file and the order used for ticket queues.
DATA_FILE = "data/tickets.json"
PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}
STATUSES = ("open", "in_progress", "resolved")
PRIORITIES = ("critical", "high", "medium", "low")


# Generate the next ticket ID without reusing IDs after tickets are reloaded.
def generate_ticket_id(tickets):
    existing_numbers = []

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if (
            isinstance(ticket_id, str)
            and ticket_id.startswith("T")
            and ticket_id[1:].isdigit()
        ):
            existing_numbers.append(int(ticket_id[1:]))

    next_number = max(existing_numbers, default=0) + 1
    return f"T{next_number:03d}"


# Sort tickets by priority first, then by their numeric ticket ID.
def sort_tickets(tickets):
    return sorted(
        tickets,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket.get("priority"), 99),
            int(ticket["id"][1:])
            if ticket.get("id", "")[1:].isdigit()
            else float("inf"),
        ),
    )


# Display one ticket in a consistent, readable format.
def display_ticket(ticket):
    print(f"\nTicket ID:       {ticket['id']}")
    print(f"Title:           {ticket['title']}")
    print(f"Category:        {ticket['category']}")
    print(f"Urgency:         {ticket['urgency']}")
    print(f"Affected users:  {ticket['affected_users']}")
    print(f"Priority:        {ticket['priority']}")
    print(f"Status:          {ticket['status']}")
    print(f"Assigned to:     {ticket['assigned_to'] or 'Unassigned'}")


# Save the current ticket collection and report any file-writing failure.
def persist_tickets(tickets):
    try:
        save_tickets(tickets, DATA_FILE)
        return True
    except OSError as error:
        print(f"Error saving tickets: {error}")
        print("The latest changes may not be saved to disk.")
        return False


# Ask for a ticket ID and return the matching ticket, handling invalid IDs.
def prompt_for_ticket(tickets):
    ticket_id = input("Enter ticket ID (e.g. T001): ").strip().upper()

    try:
        return get_ticket(tickets, ticket_id)
    except ValueError as error:
        print(f"Error: {error}")
        return None


# Create a ticket, add it to the collection, and persist the change.
def create_ticket_action(tickets):
    print("\n--- Create Ticket ---")

    title = input("Title: ").strip()
    category = input("Category (Network/Hardware/Software/Other): ").strip().lower()
    urgency = input("Urgency (low/medium/high): ").strip().lower()

    try:
        affected_users = int(input("Number of affected users: ").strip())

        ticket = create_ticket(
            generate_ticket_id(tickets),
            title,
            category,
            urgency,
            affected_users,
        )

        add_ticket(tickets, ticket)
        display_ticket(ticket)
        persist_tickets(tickets)

    except ValueError as error:
        print(f"Could not create ticket: {error}")


# Display all tickets in priority order, including resolved tickets.
def list_tickets_action(tickets):
    print("\n--- All Tickets ---")

    ordered_tickets = sort_tickets(list_tickets(tickets))

    if not ordered_tickets:
        print("No tickets found.")
        return

    for ticket in ordered_tickets:
        print(
            f"{ticket['id']} | {ticket['priority'].upper():8} | "
            f"{ticket['status']:12} | {ticket['title']}"
        )


# Find and display the details of one ticket.
def view_ticket_action(tickets):
    print("\n--- View Ticket ---")
    ticket = prompt_for_ticket(tickets)

    if ticket is not None:
        display_ticket(ticket)


# Assign an unassigned ticket to a staff member.
def assign_ticket_action(tickets):
    print("\n--- Assign Ticket ---")
    ticket = prompt_for_ticket(tickets)

    if ticket is None:
        return

    staff_name = input("Staff member's name: ").strip()

    try:
        assign_ticket(tickets, ticket["id"], staff_name)
        print(f"Ticket {ticket['id']} assigned to {ticket['assigned_to']}.")
        persist_tickets(tickets)
    except (ValueError, AttributeError) as error:
        print(f"Could not assign ticket: {error}")


# Update ticket status while enforcing the existing workflow rules.
def update_ticket_status_action(tickets):
    print("\n--- Update Ticket Status ---")
    ticket = prompt_for_ticket(tickets)

    if ticket is None:
        return

    print("Available statuses: open, in_progress, resolved")
    new_status = input("New status: ").strip().lower()

    try:
        update_status(tickets, ticket["id"], new_status)
        print(f"Ticket {ticket['id']} status updated to {new_status}.")
        persist_tickets(tickets)
    except ValueError as error:
        print(f"Could not update status: {error}")


# Show counts for every status and priority, including categories with zero tickets.
def display_reports(tickets):
    print("\n--- Ticket Reports ---")
    print(f"Total tickets: {len(tickets)}")

    print("\nBy status:")
    for status in STATUSES:
        count = sum(ticket.get("status") == status for ticket in tickets)
        print(f"  {status}: {count}")

    print("\nBy priority:")
    for priority in PRIORITIES:
        count = sum(
            ticket.get("priority") == priority for ticket in tickets
        )
        print(f"  {priority}: {count}")

    print("\n--- Unresolved Ticket Queue ---")
    unresolved = [
        ticket for ticket in tickets
        if ticket.get("status") != "resolved"
    ]

    for ticket in sort_tickets(unresolved):
        print(
            f"{ticket['id']} | {ticket['priority'].upper():8} | "
            f"{ticket['status']:12} | {ticket['title']}"
        )

    if not unresolved:
        print("No unresolved tickets.")


# Display the main menu and its available actions.
def display_menu():
    print("\n========== CampusFlow Helpdesk ==========")
    print("1. Create ticket")
    print("2. List tickets")
    print("3. View ticket")
    print("4. Assign ticket")
    print("5. Update ticket status")
    print("6. View reports")
    print("0. Exit")
    print("=========================================")


# Load tickets, run the menu until exit, and handle startup errors safely.
def main():
    try:
        tickets = load_tickets(DATA_FILE)
    except (ValueError, OSError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Fix the ticket file before restarting. No data was overwritten.")
        return

    print(f"CampusFlow started. Tickets loaded: {len(tickets)}")

    while True:
        display_menu()

        try:
            choice = input("Choose an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting CampusFlow.")
            break

        if choice == "1":
            create_ticket_action(tickets)
        elif choice == "2":
            list_tickets_action(tickets)
        elif choice == "3":
            view_ticket_action(tickets)
        elif choice == "4":
            assign_ticket_action(tickets)
        elif choice == "5":
            update_ticket_status_action(tickets)
        elif choice == "6":
            display_reports(tickets)
        elif choice == "0":
            print("Exiting CampusFlow.")
            break
        else:
            print("Invalid option. Choose a number from 0 to 6.")


# Start CampusFlow only when main.py is executed directly.
if __name__ == "__main__":
    main()
