import random
import mysql.connector  # {{ edit_1 }}


def generate_feedbacks(feedback_num):
    feedback_content = [
        'Thank you for your review!',
        'We appreciate your feedback.',
        'Your review helps us improve our events.',
        'We are glad you enjoyed the event!',
        'Thank you for your support.',
    ]
    feedback_list = []

    for i in range(feedback_num):
        feedback = {
            'review_id': (i + 1),
            'feedback_content': random.choice(feedback_content)
        }
        feedback_list.append(feedback)

    return feedback_list


def insert_feedbacks(feedbacks, cursor, conn):
    print("Inserting feedbacks into the database...")
    insert_query = """
    INSERT INTO `Feedback` (
        `review_id`, `feedback_content`
    ) VALUES (%s, %s)
    """
    try:
        # Prepare feedback values as tuples
        feedback_values = [(f['review_id'], f['feedback_content']) for f in feedbacks]
        
        # Use executemany to insert all at once
        cursor.executemany(insert_query, feedback_values)

        conn.commit()  # Commit all inserts at once
        print(f"Inserted {len(feedbacks)} feedbacks successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        conn.rollback()  # Roll back in case of error