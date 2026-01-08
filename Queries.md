# Monthly average passenger volume 
```
SELECT
    CAST(SUBSTRING("Activity Period Start Date", 6, 2) AS INTEGER) AS month,
    AVG("Passenger Count") AS avg_passengers
FROM "AwsDataCatalog"."flight_db"."raw"
GROUP BY CAST(SUBSTRING("Activity Period Start Date", 6, 2) AS INTEGER)
ORDER BY month;
```
# Monthly Passenger Volume Associated with Weather Conditions in Each Airport
```
WITH weather_mapped AS (
    SELECT *,
      CASE
        WHEN lat BETWEEN 35 AND 36 AND lon BETWEEN -117 AND -116 THEN 'CA'
        WHEN lat BETWEEN 34 AND 35 AND lon BETWEEN -98 AND -97 THEN 'AS'
        WHEN lat BETWEEN 34 AND 35 AND lon BETWEEN -113 AND -112 THEN 'AZ'
        WHEN lat BETWEEN 38 AND 39 AND lon BETWEEN -102 AND -101 THEN 'AA'
        WHEN lat BETWEEN 46 AND 47 AND lon BETWEEN -118 AND -117 THEN 'WN'
        ELSE 'UNKNOWN'
      END AS airport_code_visible
    FROM flight_db.weather_merged_v2
)

SELECT
    f."Operating Airline IATA Code" AS airport_code,

    CAST(f."Activity Period" / 100 AS INTEGER) AS year,
    CAST(f."Activity Period" % 100 AS INTEGER) AS month,

    SUM(f."Passenger Count") AS total_passengers,
    AVG(w.temp) AS avg_temp,
    AVG(w.wind_speed) AS avg_wind_speed,
    AVG(w.humidity) AS avg_humidity

FROM flight_db.raw f
JOIN weather_mapped w
  ON f."Operating Airline IATA Code" = w.airport_code_visible
 AND CAST(f."Activity Period" / 100 AS INTEGER) = w.year
 AND CAST(f."Activity Period" % 100 AS INTEGER) = w.month

GROUP BY
    f."Operating Airline IATA Code",
    CAST(f."Activity Period" / 100 AS INTEGER),
    CAST(f."Activity Period" % 100 AS INTEGER)

ORDER BY
    airport_code, year DESC, total_passengers DESC;
```
# Yearly passenger volume per airlines
```
SELECT 
    "Operating Airline" AS airline,
    SUBSTRING("Activity Period Start Date", 1, 4) AS year,
    SUM("Passenger Count") AS total_passengers
FROM "AwsDataCatalog"."flight_db"."raw"
GROUP BY "Operating Airline", SUBSTRING("Activity Period Start Date", 1, 4)
ORDER BY year DESC, total_passengers DESC;
```


