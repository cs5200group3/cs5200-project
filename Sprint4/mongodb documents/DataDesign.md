# Data Design Document for MongoDB Integration

## Overview
This document outlines the integration of MongoDB and MySQL within our application, detailing the design decisions made to ensure efficient data management and retrieval.

## Database Selection
- **MongoDB** was chosen for its flexibility in handling unstructured data and its ability to scale horizontally. This is particularly beneficial for our application, which requires dynamic data models that may evolve over time.
- **MySQL** was retained for structured data that benefits from ACID compliance, such as user authentication and transactional data. This ensures data integrity and reliability for critical operations.

## Data Model Design
### MongoDB Collections
1. **Concert Performers Collection**
   - **Fields**: `_id`, `number`, `name`, `bio`, `website`, `wikipediaLink`, `images`
   - **Purpose**: Store performer details, including biography, website, and images, allowing for easy retrieval and updates.

2. **Sports Players Collection**
   - **Fields**: `_id`, `number`, `name`, `bio`, `website`, `wikipediaLink`, `images`
   - **Purpose**: Store player details, including biography, website, and images, allowing for easy retrieval and updates.

3. **Family Shows Collection**
   - **Fields**: `_id`, `number`, `name`, `bio`, `website`, `wikipediaLink`, `images`
   - **Purpose**: Store family show details, including biography, website, and images, allowing for easy retrieval and updates.

4. **Arts & Theatre & Comedy Performers Collection**
   - **Fields**: `_id`, `number`, `name`, `bio`, `website`, `wikipediaLink`, `images`
   - **Purpose**: Store arts & theatre & comedy details, including biography, website, and images, allowing for easy retrieval and updates.

## Design Decisions
- The `number` field in each collection corresponds to the `event_id` in the SQL database's `event` table. This ensures a direct relationship between the data in MongoDB and the SQL database, allowing for seamless synchronization and query capabilities.

- Each collection is named after the category of performers it contains, making it easier to identify and query the relevant data.
    