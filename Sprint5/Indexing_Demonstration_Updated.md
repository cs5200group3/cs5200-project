
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
- **Details**:
  - Query uses nested loop joins, resulting in higher execution time.
  - Key fields like `ot.order_id`, `ot.ticket_id`, and `t.event_id` do not use indexes effectively.

#### Step 3: Implement Indexes
The `user` column in the `Order` table already had an existing index, which was effectively utilized to optimize Query 1 without requiring additional indexing. Additionally, the following indexes were added:
```sql
ALTER TABLE OrderTicket ADD INDEX idx_order_id (order_id);
ALTER TABLE OrderTicket ADD INDEX idx_ticket_id (ticket_id);
ALTER TABLE Ticket ADD INDEX idx_event_id (event_id);
```

### Step 4: Assess Query Performance (After Indexing)
- **Details**:
  - Execution time significantly reduced.
  - Indexes on `order_id`, `ticket_id`, and `event_id` enabled efficient lookups.

### Step 5: Comparison of Results
| Metric                | Before Indexing      | After Indexing      |
|-----------------------|----------------------|---------------------|
| Execution Time (ms)   | 4.805 - 4.838       | 0.072 - 0.108       |
| Rows Scanned          | 36 rows             | 36 rows             |
| Query Plan Efficiency | Nested Loop Joins    | Indexed Lookups     |

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
- **Details**:
  - High execution time due to full table scans and inefficient aggregation.

### Step 3: Reuse Existing Indexes
The indexes optimized in Query 1 (`idx_order_id`, `idx_ticket_id`, and `idx_event_id`) were reused effectively to support the aggregation and grouping operations in Query 2. Additionally, the `user` column in the `Order` table already had an existing index (`idx_user`), which further optimized the query by enabling efficient grouping and filtering. No new indexes were required, as the existing ones fully covered the query’s needs.

### Step 4: Assess Query Performance (After Indexing)
- **Details**:
  - Execution time significantly reduced.
  - Indexes enabled efficient grouping and aggregation.

### Step 5: Comparison of Results
| Metric                | Before Indexing      | After Indexing      |
|-----------------------|----------------------|---------------------|
| Execution Time (ms)   | ~14.783             | ~7.647             |
| Rows Scanned          | ~2045 rows          | ~2045 rows         |
| Query Plan Efficiency | Full Table Scan      | Indexed Lookups     |

---

## Conclusion
The addition of proper indexing for both queries significantly improved performance by reducing execution time and enabling indexed lookups for joins and aggregations. This demonstrates the critical importance of indexing in database query optimization.
