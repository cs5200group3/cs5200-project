# Restructured Persona Requirements Summary

## 1. Emma Thompson (Marketing Specialist, Customer)

### Key Tasks:
- Search for and purchase event tickets
- Manage account preferences
- Request refunds
- Receive notifications about events and changes

### Important Entities and Attributes:

- Account
  - account_id
  - username
  - email
  - phone
  - accessibility_needs
  - social_media_link

- UserGenre
  - user_genre_id
  - user
  - genre_id

- UserNotificationType
  - user_notification_type_id
  - user
  - notification_type_id
  - is_enabled

- Order
  - order_id
  - user
  - order_time
  - order_total
  - order_status
  - refund_requested

- Ticket
  - ticket_id
  - order_id
  - event_id
  - user
  - ticket_type
  - current_price
  - perks
  - sold

- Event
  - event_id
  - event_name
  - event_date
  - event_start_time
  - event_end_time
  - event_location
  - event_description
  - event_genre

- Refund
  - refund_id
  - order_id
  - payment_id
  - refund_amount
  - refund_time
  - refund_status
  - refund_reason

- Payment
  - payment_id
  - payment_status
  - payment_time
  - payment_method
  - refunded

- Review
  - review_id
  - event_id
  - user
  - review_content
  - review_date
  - review_status

- Notification
  - notification_id
  - event_id
  - notification_type
  - notification_content
  - notification_sent_sent_time
 
- Userrequest
  - user_request_id
  - requester_acount_id
  - processer_account_id
  - requested_action
  - Request_time
  - reply_message
  - reply_time
  - Addressed

- Genre
  - genre_id
  - genre_name

## 2. Lucas Ramirez (Event Coordinator)

### Key Tasks:
- Create and manage events
- Monitor ticket sales and metrics
- Communicate with attendees
- Manage different ticket types and pricing

### Important Entities and Attributes:

- Event
  - event_id
  - organizer
  - event_name
  - event_date
  - event_start_time
  - event_end_time
  - event_location
  - event_description
  - event_genre
  - total_tickets
  - tickets_sold
  - revenue_earned

- Ticket
  - ticket_id
  - event_id
  - ticket_type
  - current_price
  - perks
  - sold

- Genre
  - genre_id
  - genre_name

- Notification
  - notification_id
  - event_id
  - notification_type
  - notification_content
  - notification_sent_sent_time

- Account (for attendees)
  - account_id
  - email
  - phone

- Order
  - order_id
  - user
  - order_time
  - order_total
  - order_status

- Review
  - review_id
  - event_id
  - user
  - review_content
  - review_date
  - review_status

- Feedback
  - feedback_id
  - review_id
  - organizer
  - feedback_content
  - feedback_date

## 3. Sophia Lee (Operations Manager at TicketNest)

### Key Tasks:
- Monitor user activity
- Manage user accounts
- Analyze performance metrics
- Process refund requests
- Moderate reviews
- Oversee platform security and data protection

### Important Entities and Attributes:

- Account
  - account_id
  - account_type
  - username
  - account_status
  - last_activity
  - account_creation_time

- Order
  - order_id
  - user
  - order_time
  - order_total
  - order_status
  - refund_requested

- Event
  - event_id
  - organizer
  - total_tickets
  - tickets_sold
  - revenue_earned

- Review
  - review_id
  - event_id
  - user
  - review_content
  - review_date
  - review_status
  - admin
  - flagged

- Refund
  - refund_id
  - order_id
  - payment_id
  - refund_amount
  - refund_time
  - refund_status
  - refund_reason
  - admin

- UserRequest
  - user_request_id
  - requester_acount_id
  - processer_account_id
  - requested_action
  - request_time
  - reply_message
  - reply_time
  - addressed

- Notification
  - notification_id
  - event_id
  - notification_type
  - notification_content
  - notification_sent_sent_time

- Payment
  - payment_id
  - payment_status
  - payment_time
  - payment_method
  - refunded

- Message
  - message_id
  - recipient
  - sender
  - message_content
  - message_time
