import random
from faker import Faker

# Function to generate synthetic events
def generate_events(num_events=100):
    print(f"Generating {num_events} synthetic events...")
    fake = Faker()
    events = []

    for _ in range(num_events):
        event = {
            'event_name': fake.catch_phrase(),
            'event_date': fake.date_this_year(),
            'event_start_time': fake.time(),
            'event_end_time': fake.time(),
            'event_location': fake.address(),
            'event_description': fake.text(max_nb_chars=65535),
            'event_genre': random.randint(1, 10),  # Assuming genres are represented by integers 1-10
            'event_status': random.choice(['Upcoming', 'Active', 'Past']),
            'total_tickets': random.randint(50, 1000),
            'tickets_sold': random.randint(0, 1000),
            'revenue_earned': round(random.uniform(0, 50000), 2),
            'accessibility': random.choice(['Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired', 'None']),
            'image_url': fake.image_url(),
            'organizer': random.randint(1, 50)  # Assuming organizers are represented by integers 1-50
        }
        events.append(event)

    print(f"Generated {len(events)} events.")
    return events

# Example usage
events = generate_events(100)
for event in events[:5]:  # Print the first 5 events to verify
    print(event)