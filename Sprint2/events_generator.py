import random
from faker import Faker


# Function to generate synthetic events
def generate_events_ticket_order(organizers, num_events=100):
    print(f"Generating {num_events} synthetic events...")
    fake = Faker()
    events = []
    tickets = []
    orders = []

    for _ in range(num_events):
        # generate total ticket number
        total_ticket = random.randint(50, 200)

        # Select a random organizer from the list
        organizer = random.choice(organizers)
        # Ensure the event date is after the organizer's account creation time
        event_date = fake.date_time_between(start_date=organizer['account_creation_time'], end_date='now')

        event = {
            'event_name': fake.catch_phrase(),
            'event_date': event_date,
            'event_start_time': fake.time(),
            'event_end_time': fake.time(),
            'event_location': fake.address(),
            'event_description': fake.text(max_nb_chars=65535),
            'event_genre': random.randint(1, 4),  # Assuming genres are represented by integers 1-10
            'total_tickets': total_ticket,
            'tickets_sold': random.randint(0, total_ticket),
            'revenue_earned': round(random.uniform(0, 50000), 2),
            'accessibility': random.choice(['Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired', 'None']),
            'image_url': fake.image_url(),
            'organizer': organizer['account_id']  # Assuming you have the account_id in the organizer data
        }
        events.append(event)


