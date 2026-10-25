from campusflow.tickets import (
    get_ticket
)

# Update a ticket's status while enforcing the workflow rules.
def update_status(tickets: list, ticket_id: str, new_status: str) -> dict:
    valid_status = ['open', 'in_progress', 'resolved']

    if new_status not in valid_status:
        raise ValueError('invalid status code!')
    my_ticket = get_ticket(tickets, ticket_id)

    if new_status == 'in_progress' and my_ticket['assigned_to'] is None:
        raise ValueError('error: ticket needs a staff memeber assigned!')

    if my_ticket['status'] == 'resolved' and new_status == 'in_progress':
        raise ValueError('error: ticket must be re_opened with: open')

    my_ticket['status'] = new_status
    return my_ticket