import random
from faker import Faker
from datetime import datetime, timedelta


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

        start_times = [
            datetime.strptime("15:00", "%H:%M").time(),  # 3:00 PM
            datetime.strptime("17:00", "%H:%M").time()   # 5:00 PM
        ]
        end_times = [
            datetime.strptime("18:00", "%H:%M").time(),  # 6:00 PM
            datetime.strptime("22:00", "%H:%M").time()   # 10:00 PM
        ]

        # Generate event description using Faker
        event_description = fake.sentence(nb_words=50)  # Generate a brief description
        event = {
            'organizer': random.randint(451, 500),
            'event_name': fake.catch_phrase(),
            'event_date': event_date,
            'event_start_time': random.choice(start_times),
            'event_end_time': random.choice(end_times),
            'event_location': fake.address(),
            'event_description': event_description,  # Use the generated description
            'event_genre': random.randint(1, 4),
            'total_tickets': total_ticket
        }
        events.append(event)
    
    genres = ['concert', 'sports', 'art, theatre & comedy', 'family']

    # Update events with real names
    for event in events:
        location = fake.city()
        event_type = genres[event['event_genre'] - 1]
        event['event_name'] = f"{location} {event_type}"

    return events


def insert_events(events, cursor, conn, batch_size=50):
    print("Inserting events into the database...")
    insert_query = """
    INSERT INTO `Event` (
        `organizer`, `event_name`, `event_date`, `event_start_time`, `event_end_time`, `event_location`, 
        `event_description`, `event_genre`, `total_tickets`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(0, len(events), batch_size):
        batch = events[i:i + batch_size]
        cursor.executemany(insert_query, [
            (
                event['organizer'],
                event['event_name'],
                event['event_date'],
                event['event_start_time'],
                event['event_end_time'],
                event['event_location'],
                event['event_description'],
                event['event_genre'],
                event['total_tickets']
            ) for event in batch
        ])
        conn.commit()  # Commit after each batch
        print(f"Inserted batch {i // batch_size + 1} successfully.")

    print("All events inserted successfully.")



