import random


def generate_feedback(feedback_num):
    feedback_content = [
        'Thank you for your review!',
        'We appreciate your feedback.',
        'Your review helps us improve our events.',
        'We are glad you enjoyed the event!',
        'Thank you for your support.',
    ]
    feedback_list = []

    for _ in range(feedback_num):
        feedback = {
            'review_id': random.randint(1, 20),
            'feedback_content': random.choice(feedback_content)
        }
        feedback_list.append(feedback)

    return feedback_list
