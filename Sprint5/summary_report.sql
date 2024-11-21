DELIMITER $$

CREATE PROCEDURE GenerateSummaryReport(
    IN start_date DATE,
    IN end_date DATE
)
BEGIN
    -- Clear previous report data
    TRUNCATE TABLE SummaryReport;

    -- Populate the reports table with aggregated data
    INSERT INTO SummaryReport (
        event_id,
        event_name,
        event_date,
        event_location,
        total_tickets_sold,
        total_revenue,
        average_rating
    )
    SELECT
        e.event_id,
        e.event_name,
        e.event_date,
        e.event_location,
        COALESCE(SUM(ot.quantity), 0) AS total_tickets_sold,
        COALESCE(SUM(t.price * ot.quantity), 0.00) AS total_revenue,
        COALESCE(MAX(ar.average_rating), 0.00) AS average_rating
    FROM 
        Event e
    LEFT JOIN 
        Ticket t ON e.event_id = t.event_id
    LEFT JOIN 
        OrderTicket ot ON t.ticket_id = ot.ticket_id
    LEFT JOIN 
        (
            SELECT 
                event_id,
                AVG(rating) AS average_rating
            FROM 
                Review
            GROUP BY 
                event_id
        ) ar ON e.event_id = ar.event_id
    WHERE 
        e.event_date BETWEEN start_date AND end_date
    GROUP BY 
        e.event_id, e.event_name, e.event_date, e.event_location;
END$$

DELIMITER ;


-- call procedure:
-- CALL GenerateSummaryReport('2024-01-01', '2024-12-31');
