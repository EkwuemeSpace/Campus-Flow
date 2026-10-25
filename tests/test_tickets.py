# Test CampusFlow's priority calculation rules using Python's unittest framework.
import unittest
from campusflow.workflow import (
    update_status
)
from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    add_ticket,
    get_ticket,
    list_tickets,
    assign_ticket,
    
)

# Import the function we want to test.
from campusflow.storage import (
    save_tickets,
    load_tickets
)
# Test finding tickets and handling missing tickets.
class TestGetTicket(unittest.TestCase):

    def setUp(self):
        # Create sample tickets for each test.
        self.tickets = [
            {"id": "T001", "title": "WiFi issue"},
            {"id": "T002", "title": "Laptop issue"},
            {"id": "T003", "title": "Printer issue"},
        ]

    def test_find_first_ticket(self):
        # Check that the first ticket can be found.
        result = get_ticket(self.tickets, "T001")
        self.assertEqual(result["title"], "WiFi issue")

    def test_find_ticket_later_in_list(self):
        # Ensure the function continues searching after a non-match.
        result = get_ticket(self.tickets, "T003")
        self.assertEqual(result["title"], "Printer issue")

    def test_missing_ticket_id(self):
        # Check that an unknown ID raises ValueError.
        with self.assertRaises(ValueError):
            get_ticket(self.tickets, "T999")

    def test_empty_ticket_list(self):
        # Check how the function handles an empty collection.
        with self.assertRaises(ValueError):
            get_ticket([], "T001")

class TestCalculatePriority(unittest.TestCase):

    def test_high_urgency_and_many_users_is_critical(self):
        self.assertEqual(calculate_priority("high", 12), "critical")

    def test_high_urgency_and_few_users_is_high(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_low_urgency_and_ten_users_is_high(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_urgency_is_medium(self):
        self.assertEqual(calculate_priority("medium", 1), "medium")

    def test_three_users_is_medium(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_urgency_and_one_user_is_low(self):
        self.assertEqual(calculate_priority("low", 1), "low")

# Test allowed and forbidden ticket status transitions.
class TestUpdateStatus(unittest.TestCase):

    def setUp(self):
        # Prepare an assigned ticket and an unassigned ticket.
        self.tickets = [
            {"id": "T001", "status": "open", "assigned_to": "Chika"},
            {"id": "T002", "status": "open", "assigned_to": None},
            {"id": "T003", "status": "resolved", "assigned_to": "Emeka"},
        ]

    def test_move_assigned_ticket_to_in_progress(self):
        # An assigned ticket can move from open to in_progress.
        result = update_status(self.tickets, "T001", "in_progress")
        self.assertEqual(result["status"], "in_progress")

    def test_reject_unassigned_ticket_in_progress(self):
        # An unassigned ticket cannot move to in_progress.
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T002", "in_progress")

    def test_resolve_ticket(self):
        # An assigned ticket can be resolved.
        result = update_status(self.tickets, "T001", "resolved")
        self.assertEqual(result["status"], "resolved")

    def test_reopen_resolved_ticket(self):
        # A resolved ticket can be reopened to open.
        result = update_status(self.tickets, "T003", "open")
        self.assertEqual(result["status"], "open")

    def test_reject_direct_restart_of_resolved_ticket(self):
        # A resolved ticket cannot move directly to in_progress.
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T003", "in_progress")

    def test_reject_invalid_status(self):
        # Statuses outside the allowed set must be rejected.
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T001", "pending")

    def test_reject_unknown_ticket(self):
        # A nonexistent ticket ID must be rejected.
        with self.assertRaises(ValueError):
            update_status(self.tickets, "T999", "resolved")

# Test listing tickets when the collection is empty or populated.
class TestListTickets(unittest.TestCase):

    def test_returns_all_tickets(self):
        # Confirm that the function returns the existing tickets.
        tickets = [
            {"id": "T001", "title": "WiFi issue"},
            {"id": "T002", "title": "Laptop issue"},
        ]
        self.assertEqual(list_tickets(tickets), tickets)

    def test_returns_empty_list(self):
        # Confirm that an empty collection produces an empty list.
        self.assertEqual(list_tickets([]), [])


# Test adding tickets and preventing duplicate ticket IDs.
class TestAddTicket(unittest.TestCase):

    def test_add_new_ticket(self):
        tickets = []
        ticket = {"id": "T001", "title": "WiFi issue"}

        add_ticket(tickets, ticket)

        self.assertEqual(len(tickets), 1)
        self.assertEqual(tickets[0], ticket)

    def test_reject_duplicate_ticket_id(self):
        existing_ticket = {"id": "T001", "title": "WiFi issue"}
        new_ticket = {"id": "T001", "title": "Laptop issue"}
        tickets = [existing_ticket]

        with self.assertRaises(ValueError):
            add_ticket(tickets, new_ticket)

        self.assertEqual(len(tickets), 1)

    def test_reject_non_list_collection(self):
        ticket = {"id": "T001", "title": "WiFi issue"}

        with self.assertRaises(ValueError):
            add_ticket({}, ticket)

    def test_reject_non_dictionary_ticket(self):
        with self.assertRaises(ValueError):
            add_ticket([], "T001")

# Test assigning tickets and rejecting invalid assignments.
class TestAssignTicket(unittest.TestCase):

    def setUp(self):
        # Prepare one unassigned ticket for each test.
        self.tickets = [
            {
                "id": "T001",
                "title": "WiFi issue",
                "assigned_to": None
            }
        ]

    def test_assign_unassigned_ticket(self):
        # Confirm that a staff member is assigned successfully.
        result = assign_ticket(self.tickets, "T001", "Chika")
        self.assertEqual(result["assigned_to"], "Chika")

    def test_reject_already_assigned_ticket(self):
        # Confirm that an existing assignee cannot be replaced.
        self.tickets[0]["assigned_to"] = "Chika"

        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "Emeka")

    def test_reject_empty_staff_name(self):
        # Confirm that an empty staff name is rejected.
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "")

    def test_reject_whitespace_staff_name(self):
        # Confirm that a staff name containing only spaces is rejected.
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T001", "   ")

    def test_reject_unknown_ticket(self):
        # Confirm that assigning a nonexistent ticket raises ValueError.
        with self.assertRaises(ValueError):
            assign_ticket(self.tickets, "T999", "Chika")

# Import tools for temporary files and unit testing.
import tempfile
import unittest
import json
from pathlib import Path



# Test that tickets are saved correctly as JSON.
class TestStorage(unittest.TestCase):
    def test_save_tickets(self):
        # Create a temporary folder for this test.
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "tickets.json"

            # Prepare one example ticket.
            tickets = [
                {
                    "id": "T001",
                    "title": "Internet is down",
                    "category": "Network",
                    "urgency": "high",
                    "affected_users": 12,
                    "priority": "critical",
                    "status": "open",
                    "assigned_to": None,
                }
            ]

            # Save the ticket to the temporary JSON file.
            save_tickets(tickets, str(file_path))

            # Read the saved file and convert its JSON back into Python data.
            with file_path.open("r", encoding="utf-8") as file:
                saved_tickets = json.load(file)

            # Confirm the saved data matches the original tickets.
            self.assertEqual(saved_tickets, tickets)
        # Check that saving creates missing parent folders automatically.
    def test_save_tickets_creates_missing_folder(self):
        # Create a temporary folder for this test.
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "data" / "tickets.json"

            # Save an empty ticket list inside the missing data folder.
            save_tickets([], str(file_path))

            # Confirm that the file was created.
            self.assertTrue(file_path.exists())

            # Confirm that the saved JSON contains an empty list.
            with file_path.open("r", encoding="utf-8") as file:
                self.assertEqual(json.load(file), [])

    
    # Check that saved tickets can be loaded correctly.
    def test_load_tickets(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "tickets.json"
            tickets = [{"id": "T001", "title": "Internet is down"}]

            # Save the sample tickets, then load them again.
            save_tickets(tickets, str(file_path))
            loaded_tickets = load_tickets(str(file_path))

            # Confirm the loaded tickets match the originals.
            self.assertEqual(loaded_tickets, tickets)

    # Check that a missing file returns an empty list.
    def test_load_missing_file(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "missing.json"

            # Confirm that loading a nonexistent file starts fresh.
            self.assertEqual(load_tickets(str(file_path)), [])

    # Check that malformed JSON raises a clear error.
    def test_load_invalid_json(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "tickets.json"

            # Write invalid JSON into the file.
            file_path.write_text("{invalid json", encoding="utf-8")

            # Confirm that invalid JSON raises ValueError.
            with self.assertRaisesRegex(ValueError, "Invalid JSON"):
                load_tickets(str(file_path))


# Test ticket creation and input validation.
class TestCreateTicket(unittest.TestCase):

    def test_create_ticket_with_valid_data(self):
        ticket = create_ticket(
            "T001", "WiFi not working", "network", "high", 12
        )
        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["title"], "WiFi not working")
        self.assertEqual(ticket["priority"], "critical")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])

    def test_create_ticket_rejects_blank_title(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "   ", "network", "low", 1)

    def test_create_ticket_rejects_invalid_urgency(self):
        with self.assertRaises(ValueError):
            create_ticket("T001", "WiFi issue", "network", "urgent", 1)

    def test_create_ticket_rejects_invalid_affected_users(self):
        for users in [0, -1, True, 2.5, "five"]:
            with self.subTest(users=users):
                with self.assertRaises(ValueError):
                    create_ticket(
                        "T001", "WiFi issue", "network", "low", users
                    )


if __name__ == "__main__":
    unittest.main()


    