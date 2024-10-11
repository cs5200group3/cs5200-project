CREATE TABLE `Account` (
	`account_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`account_type` ENUM('user', 'organizer', 'admin'),
	`username` VARCHAR(255),
	`password` VARCHAR(255),
	`first_name` VARCHAR(255),
	`last_name` VARCHAR(255),
	`email` VARCHAR(255),
	`phone` VARCHAR(255),
	`account_status` ENUM('Active', 'Inactive'),
	`last_activity` DATETIME,
	`account_creation_time` DATETIME,
	PRIMARY KEY(`account_id`)
);


CREATE TABLE `Genre` (
	`genre_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`genre_name` VARCHAR(255),
	PRIMARY KEY(`genre_id`)
);


CREATE TABLE `NotificationType` (
	`notification_type_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`notification_type` VARCHAR(255),
	PRIMARY KEY(`notification_type_id`)
);


CREATE TABLE `UserGenre` (
	`user` INTEGER,
	`genre_id` INTEGER,
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


CREATE TABLE `Payment` (
	`payment_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
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
	`total_tickets` INTEGER,
	PRIMARY KEY(`event_id`),
	FOREIGN KEY(`organizer`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`event_genre`) REFERENCES `Genre`(`genre_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for genre
);

CREATE TABLE `Order` (
	`order_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`payment_id` INTEGER,
	`user` INTEGER,
	`order_time` DATETIME,
	`order_total` DECIMAL,
	`order_status` ENUM('Confirmed', 'Refunded'),
	`event_id` INTEGER,
	`ticket_type` ENUM('General Admission', 'VIP'),
	`current_price` DECIMAL,
	PRIMARY KEY(`order_id`),
	FOREIGN KEY(`user`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,
	FOREIGN KEY(`payment_id`) REFERENCES `Payment`(`payment_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION, -- No cascade for payment
	FOREIGN KEY(`event_id`) REFERENCES `Event`(`event_id`)
		ON UPDATE CASCADE ON DELETE CASCADE  -- Cascading delete for event
);


CREATE TABLE `Notification` (
	`notification_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`event_id` INTEGER,
	`notification_type_id` INTEGER,
	`notification_content` TEXT(65535),
	PRIMARY KEY(`notification_id`),
	FOREIGN KEY(`event_id`) REFERENCES `Event`(`event_id`)
		ON UPDATE CASCADE ON DELETE CASCADE,  -- Cascading delete for event
	FOREIGN KEY(`notification_type_id`) REFERENCES `NotificationType`(`notification_type_id`)
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
	`review_id` INTEGER,
	`feedback_content` TEXT(65535),
	PRIMARY KEY(`feedback_id`),
	FOREIGN KEY(`review_id`) REFERENCES `Review`(`review_id`) ON UPDATE NO ACTION ON DELETE NO ACTION
);

CREATE TABLE `Refund` (
	`refund_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`payment_id` INTEGER,
	`refund_status` ENUM('Approved', 'Rejected'),
	`refund_reason` TEXT(65535),
	`admin` INTEGER,
	PRIMARY KEY(`refund_id`),
	FOREIGN KEY(`payment_id`) REFERENCES `Payment`(`payment_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION,  -- No cascade for payment
	FOREIGN KEY(`admin`) REFERENCES `Account`(`account_id`)
		ON UPDATE NO ACTION ON DELETE NO ACTION  -- No cascade for admin
);

CREATE TABLE `UserRequest` (
	`user_request_id` INTEGER NOT NULL AUTO_INCREMENT UNIQUE,
	`requester_account_id` INTEGER,
	`processer_account_id` INTEGER,
	`requested_action` ENUM('Activate', 'Deactivate'),
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

