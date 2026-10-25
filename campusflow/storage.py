from pathlib import Path
import json

# Save the current ticket collection to a JSON file.
# Import tools for working with file paths and JSON data.
from pathlib import Path
import json


# Save the current ticket collection to a JSON file.
def save_tickets(tickets: list, file_path: str) -> None:
    # Convert the supplied file path string into a Path object.
    path = Path(file_path)

    # Create the parent folder if it does not already exist.
    path.parent.mkdir(parents=True, exist_ok=True)

    # Open the file in write mode and save the tickets as readable JSON.
    with path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)

# Load tickets from a JSON file, or return an empty list if the file is missing.
def load_tickets(file_path: str) -> list:
    # Convert the supplied file path into a Path object.
    path = Path(file_path)

    # Start with an empty ticket list if the file does not exist.
    if not path.exists():
        return []

    # Open the existing file and read its JSON data.
    try:
        with path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)
    except json.JSONDecodeError as error:
        # Raise a clear error instead of silently discarding malformed data.
        raise ValueError(f"Invalid JSON in ticket file: {path}") from error

    # Ensure the loaded JSON contains a list of tickets.
    if not isinstance(tickets, list):
        raise ValueError(f"Ticket file must contain a JSON list: {path}")

    # Return the tickets loaded from the file.
    return tickets