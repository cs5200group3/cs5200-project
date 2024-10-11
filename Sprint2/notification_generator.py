import mysql.connector
import random
from datetime import datetime, timedelta

# Lists for notification content, one list per notification_type_id (1-5)
notification_content_lists = {
    1: ["System Maintenance Notification Dear User, there will be scheduled maintenance on our servers after 10:00 PM. Please expect temporary service disruptions. Thank you for your understanding.",
        "New Version Available A new version of our app is available! Update now to enjoy new features and improved performance.",
        "Password Change Alert Your account password was successfully changed. If this wasn’t you, please contact support immediately.",
        "System Outage Detected We are experiencing unexpected downtime. Our team is working to restore services as quickly as possible.",
        "Security Update Required For your safety, please install the latest security patch on your system. Update now to stay protected.",
        "Account Deactivation Warning Your account has been inactive for 6 months. Log in before October 20th to avoid deactivation.",
        "Data Backup Completed Your recent data backup has been successfully completed. Thank you for using our backup service.",
        "Two-Factor Authentication Enabled Two-factor authentication has been successfully activated on your account. This adds an extra layer of security.",
        "Unusual Login Attempt We detected an unusual login attempt from a new device. If this was not you, please secure your account immediately.",
        "System Resources Exceeded Your system resources usage has exceeded the allocated limit. Please upgrade your plan to avoid disruptions."
        ],
    
    2: ["Limited-Time Discount Just for You! Save 30% on your next purchase with code: FLASH30. Offer ends in 48 hours!",
        "Referral Bonus: Earn $10 Refer a friend and both of you will earn $10 in rewards when they make their first purchase.",
        "Exclusive Event Access Get early access to our exclusive event! Book your tickets now to secure your spot.",
        "Early Access to Black Friday Deals: Get early access to our Black Friday deals.",
        "New Event Just Dropped: Check out our latest collection! Be the first to explore our new arrivals and get 10% off.",
        "RSVP for Our Annual Gala: You’re invited to our Annual Gala on November 5th! RSVP by October 20th to secure your spot.",
        "Exclusive Event: Product Launch: Be the first to experience our new product at our launch event on October 20th. Limited seats available.",
        "Early Bird Tickets Now Available: Get early bird tickets for our upcoming concert at a special price! Offer ends soon.",
        "Charity Fun Run: Support a great cause by joining our charity fun run on October 30th. Register today!",
        ],

    3: ["Order Confirmation: Thank you for your purchase! Your order has been confirmed and is being processed.",
        "Order Cancellation Request Received. We have received your request to cancel order . You will be updated once the cancellation is processed.",
        "Payment Confirmation: Your payment for order has been successfully processed.",
        "Return Request Approved. Your return request has been approved. You will receive further instructions shortly."
        ],

    4: ["Concert Reminder: Live Music Tonight. Your ticket for tonight's concert is confirmed! Don't forget to bring your printed ticket for entry.",
        "Event Cancellation Notice: The event has been canceled due to unforeseen circumstances. Refunds will be processed shortly.",
        "Event Rescheduling Alert: The event has been rescheduled to a new date. Your ticket is still valid for the new date.",
        "Event Update: New Performer Added. Exciting news! A new performer has been added to the event lineup. Get ready for an amazing show."
        ],

    5: ["Event Feedback Request: We hope you enjoyed the event! Share your feedback with us to help us improve future events.",
        "Review Reminder: Your opinion matters! Don't forget to leave a review for the event you attended.",
        "Review Thank You: Thank you for your review! Your feedback helps us improve our events and services.",
        "Rating Request: How would you rate your experience at the event? Share your rating with us.",
        "Review Reminder: Your feedback is valuable to us! Share your thoughts on the event you attended.",
        "Rate Your Event : We’d love to hear your thoughts! Please take a moment to rate the event you recently participated.",
        "Write a Review and Get 10% Off : Share your feedback on your recent order and receive 10% off your next ticket!",
        "Tell Us About Your Experience : How was your recent shopping experience? Leave a review and help us improve.",
        "Your Opinion Matters: We value your feedback. Share your thoughts to help us serve you better.",
        "Review and Win! : Write a review for a chance to win a $50 gift card! Share your experience today.",
        "Review Our Service : How was your experience with our customer service? Please leave a review to let us know."
        ]
}

# Function to generate random notifications
def generate_notifications(valid_event_ids, num_notifications=100):
    notifications = []
    
    for _ in range(num_notifications):
        # Random event_id from valid_event_ids
        event_id = random.choice(valid_event_ids)
        
        # Random notification_type_id between 1 and 5
        notification_type_id = random.randint(1, 5)
        
        # Random notification_content based on the notification_type_id
        notification_content = random.choice(notification_content_lists[notification_type_id])
        
    
        
        # Append the generated notification tuple to the list
        notifications.append((event_id, notification_type_id, notification_content))
    
    return notifications

# Function to insert notifications into the Notification table
def insert_notifications(notifications, cursor, conn, batch_size=50):
    print("Inserting notifications into the database...")
    insert_query = """
    INSERT INTO `Notification` (`event_id`, `notification_type_id`, `notification_content`)
    VALUES (%s, %s, %s)
    """
    for i in range(0, len(notifications), batch_size):
        batch = notifications[i:i + batch_size]
        cursor.executemany(insert_query, batch)
        conn.commit()  # Commit the transaction after each batch

# Database connection configuration (adjust these parameters)
db_config = {
    'host': 'g3-sprint2-just4thedreamland-5e30.h.aivencloud.com',  # Replace with your Aiven hostname
    'port': 26740, 
    'user': 'avnadmin',  # Replace with your Aiven username
    'password': 'AVNS_k8-EKEKB0de1fhIa09w',  # Replace with your Aiven password
    'database': 'sprint2'  # Replace with your database name
}

# Connect to the database
def connect_to_database():
    print("Connecting to the database...")
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    print("Database connection established.")
    return conn, cursor

# Fetch valid event_ids from the Event table
def fetch_valid_event_ids(cursor):
    cursor.execute("SELECT event_id FROM Event")
    result = cursor.fetchall()
    return [row[0] for row in result]

# Main function to generate and insert notifications
def generate_and_insert_notifications(num_notifications=100):
    conn, cursor = connect_to_database()
    try:
        # Fetch valid event_ids
        valid_event_ids = fetch_valid_event_ids(cursor)
        
        # Generate the random notifications
        notifications = generate_notifications(valid_event_ids, num_notifications=num_notifications)
        
        # Insert the notifications into the database
        insert_notifications(notifications, cursor, conn)
        
        print("Data insertion complete.")
    finally:
        cursor.close()
        conn.close()
        print("Database connection closed.")

if __name__ == "__main__":
    generate_and_insert_notifications(num_notifications=100)
