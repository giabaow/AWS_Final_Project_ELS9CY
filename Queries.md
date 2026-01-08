#Monthly
```
SELECT
    CAST(SUBSTRING("Activity Period Start Date", 6, 2) AS INTEGER) AS month,
    AVG("Passenger Count") AS avg_passengers
FROM "AwsDataCatalog"."flight_db"."raw"
GROUP BY CAST(SUBSTRING("Activity Period Start Date", 6, 2) AS INTEGER)
ORDER BY month;
```

