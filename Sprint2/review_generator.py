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


def generate_reviews(events, num_reviews=10):
    fake = Faker()
    reviews = []
    admin_id = 501
    print("Generating reviews...")
    for i, event in enumerate(events):
        for _ in range(num_reviews):
            rating = random.randint(1, 5)
            review_content = generate_review_content(event['event_name'], rating)
            review_status = 'Approved' if random.random() < 0.9 else random.choice(['Rejected'])

            review = {
                'event_id': (i + 1),
                'rating': rating,
                'user': random.randint(1, 450),
                'review_content': review_content,
                'review_date': fake.date_time_this_year(),
                'review_status': review_status,
                'admin': admin_id,
                'flagged': random.choice([0, 1]),
            }
            reviews.append(review)
    print("Reviews generated successfully.")
    return reviews


def insert_reviews(reviews, cursor, conn, batch_size=100):
    print("Inserting reviews into the database...")
    insert_query = """
    INSERT INTO `Review` (
        `event_id`, `rating`, `user`, `review_content`, `review_date`, `review_status`, `admin`, `flagged`
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    for i in range(0, len(reviews), batch_size):
        batch = reviews[i:i + batch_size]
        values = [
            (
                review['event_id'],
                review['rating'],
                review['user'],
                review['review_content'],
                review['review_date'],
                review['review_status'],
                review['admin'],
                review['flagged']
            )
            for review in batch
        ]
        try:
            cursor.executemany(insert_query, values)
            conn.commit()
            print(f"Inserted batch {i // batch_size + 1} successfully.")
        except mysql.connector.Error as err:
            print(f"Error inserting batch {i // batch_size + 1}: {err}")
            conn.rollback()

# # print 5 reviews
# organizers = generate_accounts(2, 'organizer')
# events = generate_events(organizers, 2)
# reviews = generate_reviews(events, 3)
# print(reviews)