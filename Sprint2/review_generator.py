import random
from faker import Faker
import openai
from events_generator import generate_events
from account_generate import generate_accounts

openai.api_key = 'sk-QkmIzlV2mFYuHgDGfFHFSc-cB9eM4mDqHvhXhIOksfT3BlbkFJHxyDgouFge9hFynqqnG_zFmQypZzWY6vSb-2FzLfcA'


# Function to generate review content using OpenAI
def generate_review_content(event_name, rating):
    prompt = f"Write a 10-15 words textreview without sepecial characters for the event '{event_name}'considering a rating of {rating} out of 5."
    
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=15
    )

    content = response.choices[0].message['content'].strip()
    return content


def generate_reviews(events, num_reviews=1000):
    fake = Faker()
    reviews = []
    admin_id = 501

    for i, event in enumerate(events):
        for _ in range(num_reviews):
            rating = random.randint(1, 5)
            review_content = generate_review_content(event['event_name'], rating)
            review_status = 'Approved' if random.random() < 0.9 else random.choice(['Flagged', 'Rejected'])

            review = {
                'event_id': (i + 1),
                'rating': rating,
                'user': random.randint(1, 450),
                'review_content': review_content,
                'review_date': fake.date_time_this_year(),
                'review_status': review_status,
                'admin': admin_id,
                'flagged': random.choice([True, False]),
            }
            reviews.append(review)
    return reviews


# print 5 reviews
organizers = generate_accounts(2, 'organizer')
events = generate_events(organizers, 2)
users = generate_accounts(5, 'user')
print(events)
reviews = generate_reviews(events, 20)
print(reviews)
