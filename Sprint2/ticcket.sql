CREATE TABLE `Account` (
	`account_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`account_type` ENUM('user', 'organizer', 'admin'),
	`username` VARCHAR(255),
	`password` VARCHAR(255),
	`first_name` VARCHAR(255),
	`last_name` VARCHAR(255),
	`email` VARCHAR(255),
	`phone` VARCHAR(255),
	`social_media_link` VARCHAR(255),
	`accessibility_needs` ENUM('Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired') COMMENT 'accessibility_needs should only be filled when account_type = ''user''',
	`account_status` ENUM('Active', 'Inactive'),
	`last_activity` DATETIME,
	`account_creation_time` DATETIME,
	PRIMARY KEY(`account_id`)
);


CREATE TABLE `Genre` (
	`genre_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`genre_name` ENUM('concert', 'sports', 'art, family & comedy', 'family'),
	PRIMARY KEY(`genre_id`)
);


CREATE TABLE `NotificationType` (
	`notification_type_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`notification_type` ENUM('System', 'Promotion', 'Order', 'Event', 'Review'),
	PRIMARY KEY(`notification_type_id`)
);


CREATE TABLE `UserGenre` (
	`genre_id` INTEGER,
	`user` INTEGER,
	PRIMARY KEY(`user`, `genre_id`),  -- Composite primary key
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for user
	FOREIGN KEY(`genre_id`) REFERENCES `Genre`(`genre_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for genre
);


CREATE TABLE `UserNotificationType` (
	`user` INTEGER,
	`notification_type_id` INTEGER,
	`is_enabled` BOOLEAN,
	PRIMARY KEY(`user`, `notification_type_id`),  -- Composite primary key
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for user
	FOREIGN KEY(`notification_type_id`) REFERENCES `NotificationType`(`notification_type_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for notification type
);


CREATE TABLE `Order` (
	`order_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`payment_id` INTEGER,
	`user` INTEGER,
	`order_time` DATETIME,
	`order_total` DECIMAL,
	`order_status` ENUM('Pending', 'Paid', 'Cancelled', 'Refunded'),
	`refund_requested` INTEGER,
	PRIMARY KEY(`order_id`),
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`payment_id`) REFERENCES `Payment`(`payment_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for payment
);


CREATE TABLE `Payment` (
	`payment_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`payment_status` ENUM('Pending', 'Paid', 'Cancelled', 'Refunded'),
	`payment_time` DATETIME,
	`payment_method` ENUM('Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay'),
	`refunded` BOOLEAN,
	PRIMARY KEY(`payment_id`)
);


CREATE TABLE `Event` (
	`event_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`organizer` INTEGER,
	`event_name` VARCHAR(255),
	`event_date` DATE,
	`event_start_time` TIME,
	`event_end_time` TIME,
	`event_location` VARCHAR(255),
	`event_description` TEXT(65535),
	`event_genre` INTEGER,
	`event_status` ENUM('Upcoming', 'Active', 'Past'),	
	`total_tickets` INTEGER,
	`tickets_sold` INTEGER,
	`revenue_earned` DECIMAL,
	`accessibility` ENUM('Wheelchair Accessible', 'Hearing Impaired', 'Visual Impaired', 'None'),
	`image_url` VARCHAR(255),
	PRIMARY KEY(`event_id`),
	FOREIGN KEY(`organizer`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`event_genre`) REFERENCES `Genre`(`genre_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for genre
);


CREATE TABLE `Ticket` (
	`ticket_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`order_id` INTEGER,
	`user` INTEGER,
	`event_id` INTEGER,
	`ticket_type` ENUM('General Admission', 'VIP'),
	`current_price` DECIMAL,
	`perks` VARCHAR(255),
	`sold` BOOLEAN,
	PRIMARY KEY(`ticket_id`),
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`event_id`) REFERENCES `Event`(`event_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for event
	FOREIGN KEY(`order_id`) REFERENCES `Order`(`order_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE TABLE `Notification` (
	`notification_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`event_id` INTEGER,
	`notification_type` ENUM('System', 'Promotion', 'Order', 'Event', 'Review'),
	`notification_content` TEXT(65535),
	`notification_sent_time` DATETIME,
	PRIMARY KEY(`notification_id`),
	FOREIGN KEY(`event_id`) REFERENCES `Event`(`event_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for event
	FOREIGN KEY(`notification_type`) REFERENCES `NotificationType`(`notification_type_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for notification type
);


CREATE TABLE `Review` (
	`review_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`event_id` INTEGER,
	`rating` INTEGER,
	`user` INTEGER,
	`review_content` TEXT(65535),
	`review_date` DATETIME,
	`review_status` ENUM('Flagged', 'Approved', 'Rejected'),
	`admin` INTEGER,
	`flagged` BOOLEAN,
	PRIMARY KEY(`review_id`),
	FOREIGN KEY(`event_id`) REFERENCES `Event`(`event_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for event
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`admin`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE TABLE `Feedback` (
	`feedback_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`organizer` INTEGER,
	`review_id` INTEGER,
	`feedback_content` TEXT(65535),
	`feedback_date` DATETIME,
	PRIMARY KEY(`feedback_id`),
	FOREIGN KEY(`organizer`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`review_id`) REFERENCES `Review`(`review_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE TABLE `Refund` (
	`refund_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`payment_id` INTEGER,
	`order_id` INTEGER,
	`refund_amount` DECIMAL,
	`refund_time` DATETIME,
	`refund_status` ENUM('Pending', 'Approved', 'Rejected'),
	`refund_reason` TEXT(65535),
	`admin` INTEGER,
	PRIMARY KEY(`refund_id`),
	FOREIGN KEY(`payment_id`) REFERENCES `Payment`(`payment_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,  -- No cascade for payment
	FOREIGN KEY(`order_id`) REFERENCES `Order`(`order_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,  -- No cascade for order
	FOREIGN KEY(`admin`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for admin
);


CREATE TABLE `UserRequest` (
	`user_request_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`requester_account_id` INTEGER,
	`processer_account_id` INTEGER,
	`requested_action` VARCHAR(255),
	`request_time` DATETIME,
	`reply_message` TEXT(65535),
	`reply_time` DATETIME,
	`addressed` BOOLEAN,
	PRIMARY KEY(`user_request_id`),
	FOREIGN KEY(`requester_account_id`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`processer_account_id`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION
);


CREATE TABLE `Message` (
	`message_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`recipient` INTEGER,
	`sender` INTEGER,
	`message_content` TEXT(65535),
	`message_time` DATETIME,
	PRIMARY KEY(`message_id`),
	FOREIGN KEY(`recipient`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`sender`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION
);