import random
from faker import Faker
import openai  # Ensure you have this import


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

        # Generate event description using OpenAI
        prompt = f"Generate a brief event description in 30 words."
        response = openai.ChatCompletion.create(
            model="gpt-4",  # or another model of your choice
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=50  # Limit the response to approximately 50 tokens
        )
        event_description = response['choices'][0]['message']['content'].strip()

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
