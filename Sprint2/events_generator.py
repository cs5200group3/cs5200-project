import random
from faker import Faker


# Function to generate synthetic events
def generate_events(organizers, num_events=100):
    print(f"Generating {num_events} synthetic events...")
    fake = Faker()
    events = []

    for _ in range(num_events):
        # Select a random organizer from the list
        organizer = random.choice(organizers)
        # Generate total ticket number
        total_ticket = random.randint(50, 200)

        # Ensure the event date is after the organizer's account creation time
        event_date = fake.date_time_between(start_date=organizer['account_creation_time'], end_date='now')

        # Generate event description using Faker
        event_description = fake.sentence(nb_words=50)  # Generate a brief description

        event = {
            'event_name': fake.catch_phrase(),
            'event_date': event_date,
            'event_start_time': fake.time(),
            'event_end_time': fake.time(),
            'event_location': fake.address(),
            'event_description': event_description,  # Use the generated description
            'event_genre': random.randint(1, 4),
            'total_tickets': total_ticket,
            'organizer': random.randint(451, 500) 
        }
        events.append(event)
    return events


def insert_events(events, cursor, conn):
    for event in events:
        try:
            cursor.execute("INSERT INTO Event (event_name, event_date, event_start_time, event_end_time, event_location, event_description, event_genre, total_tickets, organizer) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", tuple(event.values()))
        except Exception as e:
            print(f"Error inserting event: {e}")  # Error handling
    conn.commit()