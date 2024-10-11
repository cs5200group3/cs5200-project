# Schema Changes from Sprint 1 to Create Table

Our schema already contains all the tables that are required by the user stories.So we do not need to create any new tables.But we made some changes to the existing tables to make the schema more concise.

## General Changes
- **Removed**: 
  - we removed the table `Message` which were not relevant to the user stories.
  - we removed some unnecessary time parameters from the tables.
  
## Genre Table
- **Changed**: 
  - `genre_name` type changed from `ENUM` to `VARCHAR(255)`.

## NotificationType Table
- **Changed**: 
  - `notification_type` type changed from `ENUM` to `VARCHAR(255)`.

## UserGenre Table
- **Changed**: 
  - `user_genre_id` column removed.
  - Added composite primary key on (`user`, `genre_id`).
  - Added foreign key reference to `Account` for `user`.

## UserNotificationType Table
- **Changed**: 
  - Added composite primary key on (`user`, `notification_type_id`).
  - Added foreign key reference to `Account` for `user`.


## Order Table
- **Changed**: 
  - intergate the ticket entity into the order entity.

## Notification Table
- **Changed**: 
  - `notification_type` column changed to `notification_type_id` with a foreign key reference to `NotificationType`.

## 10. Review Table
- **Changed**: 
  - Added `rating` column.

# Normalization to 3NF
We have checked the schema with the 3NF form, and found that the schema is already in 3NF.
To be more concise, we removed the `user_genre_id` column from the `UserGenre` table and added a composite primary key on (`user`, `genre_id`).
