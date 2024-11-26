
# Performance Optimization with Indexing

## Query 1: Optimizing Joins

### Step 1: Identify the Slow Query
```sql
SELECT 
    o.order_id, 
    o.order_time, 
    e.event_name, 
    t.ticket_type, 
    ot.quantity
FROM `Order` o
JOIN OrderTicket ot ON o.order_id = ot.order_id
JOIN Ticket t ON ot.ticket_id = t.ticket_id
JOIN Event e ON t.event_id = e.event_id
WHERE o.user = 1
LIMIT 0, 25;
```
- **Observation**: This query involves multiple joins across `Order`, `OrderTicket`, `Ticket`, and `Event`, which can become slow as table sizes grow.

### Step 2: Assess Query Performance (Before Indexing)
Using `EXPLAIN SELECT`, the following issues were identified and analyzed to pinpoint optimization needs:
- **OrderTicket** table was performing full table scans (`ALL` in the `type` column), indicating a lack of index usage.
- Other joins also lacked efficient index usage, which contributed to slower execution times and increased resource usage.
- The detailed EXPLAIN output helped highlight these inefficiencies, guiding the decision to add indexes on join and grouping keys.

| Metric                | Value                 |
|-----------------------|-----------------------|
| Execution Time (s)    | ~0.98                |
| Rows Scanned          | ~2,000 rows          |
| Query Plan Efficiency | Full Table Scans      |
Using `EXPLAIN SELECT`, the following issues were identified:
- **OrderTicket** table was performing full table scans (`ALL` in the `type` column).
- Other joins lacked efficient index usage, resulting in increased execution time.

| Metric                | Value                 |
|-----------------------|-----------------------|
| Execution Time (s)    | ~0.98                |
| Rows Scanned          | ~2,000 rows          |
| Query Plan Efficiency | Full Table Scans      |

### Step 3: Implement Indexes
The following indexes were added to optimize the query:
```sql
ALTER TABLE OrderTicket ADD INDEX idx_order_id (order_id);
ALTER TABLE OrderTicket ADD INDEX idx_ticket_id (ticket_id);
ALTER TABLE Ticket ADD INDEX idx_event_id (event_id);
```

### Step 4: Assess Query Performance (After Indexing)
Using `EXPLAIN SELECT` after indexing, the following improvements were observed:
- **OrderTicket** now uses the `idx_order_id` index for lookups, reducing the number of rows scanned from ~2,000 to ~36.
- All joins leverage appropriate indexes, significantly reducing execution time.
- The query plan showed a shift from `ALL` (full table scan) to `ref` (indexed lookups), demonstrating optimized performance.

| Metric                | Value                 |
|-----------------------|-----------------------|
| Execution Time (s)    | ~0.072               |
| Rows Scanned          | ~36 rows             |
| Query Plan Efficiency | Indexed Lookups      |

### Step 5: Comparison of Results
| Metric                | Before Indexing      | After Indexing      |
|-----------------------|----------------------|---------------------|
| Execution Time (s)    | ~0.98               | ~0.072             |
| Rows Scanned          | ~2,000 rows         | ~36 rows           |
| Query Plan Efficiency | Full Table Scans     | Indexed Lookups     |

---

## Query 2: Optimizing Aggregation

### Step 1: Identify the Slow Query
```sql
SELECT 
    o.user, 
    COUNT(o.order_id) AS total_orders, 
    SUM(ot.quantity) AS total_tickets
FROM `Order` o
JOIN OrderTicket ot ON o.order_id = ot.order_id
GROUP BY o.user;
```
- **Observation**: This query involves aggregation (`COUNT` and `SUM`) and grouping, which can become slow without appropriate indexes.

### Step 2: Assess Query Performance (Before Indexing)
Using `EXPLAIN SELECT`, the following issues were identified:
- The query performed full table scans on `OrderTicket`, and grouping operations lacked indexed support.
- Execution time and resource usage were high due to unoptimized scans.

| Metric                | Value                 |
|-----------------------|-----------------------|
| Execution Time (s)    | ~1.12                |
| Rows Scanned          | ~2,000 rows          |
| Query Plan Efficiency | Full Table Scans      |

### Step 3: Reuse Existing Indexes
The indexes added for Query 1 (`idx_order_id`, `idx_ticket_id`, and `idx_event_id`) were reused effectively to support Query 2. Additionally, the `user` column in the `Order` table already had an existing index (`idx_user`), which further optimized the query by enabling efficient grouping and filtering.

### Step 4: Assess Query Performance (After Indexing)
Using `EXPLAIN SELECT` after indexing, the following improvements were observed:
- Grouping and aggregation operations were significantly improved due to indexed lookups.

| Metric                | Value                 |
|-----------------------|-----------------------|
| Execution Time (s)    | ~0.078               |
| Rows Scanned          | ~407 rows            |
| Query Plan Efficiency | Indexed Lookups      |

### Step 5: Comparison of Results
| Metric                | Before Indexing      | After Indexing      |
|-----------------------|----------------------|---------------------|
| Execution Time (s)    | ~1.12               | ~0.078             |
| Rows Scanned          | ~2,000 rows         | ~407 rows          |
| Query Plan Efficiency | Full Table Scans     | Indexed Lookups     |

---

## Conclusion
The addition of proper indexing for both queries significantly improved performance by reducing execution time and enabling indexed lookups for joins and aggregations. The use of `EXPLAIN SELECT` was critical in identifying inefficiencies and verifying improvements, demonstrating the importance of indexing in database optimization.
