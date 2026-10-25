# Calculate a ticket's priority from its urgency and the number of affected users.
def calculate_priority(urgency: str, affected_users: int) -> str:
    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return 'high'
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"



def create_ticket(ticket_id, title, category, urgency, affected_users):
    valid_category = ['network', 'hardware', 'software', 'other']
    valid_urgency = ['low', 'medium', 'high']

    if not isinstance(title, str) or isinstance(title, bool) or not title.strip():
        raise ValueError('error: title cannot be empty!')

    if not isinstance(affected_users, int) or isinstance(affected_users, bool) or affected_users < 1:
        raise ValueError('error: affected users must be a valid number!')
    
    if urgency not in valid_urgency:
        raise ValueError('error: invaiid urgency detected!')
    
    if category not in valid_category:
        raise ValueError('error: invlid category detected!')

    return {
        'id': ticket_id,
        'title': title.strip(),
        'category': category.capitalize(),
        'urgency': urgency,
        "affected_users": affected_users,
        'priority': calculate_priority(urgency, affected_users),
        'status': 'open',
        'assigned_to': None
    }

def add_ticket(tickets: list, ticket: dict):
    if not isinstance(tickets, list):
        raise ValueError('error, ticket must be a list!')

    if not isinstance(ticket, dict):
        raise ValueError('error: ticket must be a dict')

    for existing_ticket in tickets:
        if existing_ticket['id'] == ticket['id']:
            raise ValueError(f'Ticket ID {ticket["id"]} already exists.')

    tickets.append(ticket)



def get_ticket(tickets: list, ticket_id: str):
    if not tickets or not  ticket_id:
        raise ValueError('error: expect 2 paramms!')
    
    for ticket in tickets:
       if ticket['id'] == ticket_id:
           return ticket  
        
    raise ValueError(f'Ticket: {ticket_id} not found!')

# Return the current collection of tickets.
def list_tickets(tickets: list) -> list:
    if not tickets:
        return []

    return tickets


# Assign an unassigned ticket to a staff member.
def assign_ticket(tickets: list, ticket_id: str, staff_name: str) -> dict:
    my_ticket = get_ticket(tickets, ticket_id)

    if not staff_name.strip():
        raise ValueError('error: staff name must be provided!')
    
    if my_ticket['assigned_to'] is None:
        my_ticket['assigned_to'] = staff_name.strip()
    else:
        raise ValueError('ticket has already been assigned to a staff memebr!')

    return my_ticket