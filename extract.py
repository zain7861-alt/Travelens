import duckdb

con = duckdb.connect("travellens.duckdb")

con.execute("""
CREATE OR REPLACE TABLE flights_cleaned AS
SELECT
    YEAR,
    MONTH,
    DAY,
    AIRLINE,
    ORIGIN_AIRPORT,
    DESTINATION_AIRPORT,
    COALESCE(DEPARTURE_DELAY, 0) AS DEPARTURE_DELAY,
    COALESCE(ARRIVAL_DELAY, 0) AS ARRIVAL_DELAY,
    DISTANCE,
    CANCELLED,
    DIVERTED,

    CASE
        WHEN CANCELLED = 1 THEN 'Cancelled'
        WHEN COALESCE(ARRIVAL_DELAY, 0) > 15 THEN 'Delayed'
        ELSE 'On Time'
    END AS FLIGHT_STATUS

FROM read_csv_auto('data/flights.csv')
LIMIT 10000
""")

print(con.execute("SELECT COUNT(*) FROM flights_cleaned").fetchone())
print(con.execute("""
    SELECT *
    FROM flights_cleaned
    LIMIT 5
""").fetchall())
print(con.execute("""
    SELECT
        AIRLINE,
        AVG(ARRIVAL_DELAY) AS AVG_DELAY
    FROM flights_cleaned
    WHERE CANCELLED = 0
    GROUP BY AIRLINE
    ORDER BY AVG_DELAY DESC
""").fetchall())
print(con.execute("""
    SELECT
        AIRLINE,
        COUNT(*) AS CANCELLED_FLIGHTS
    FROM flights_cleaned
    WHERE CANCELLED = 1
    GROUP BY AIRLINE
    ORDER BY CANCELLED_FLIGHTS DESC
""").fetchall())
print(con.execute("""
    SELECT
        ORIGIN_AIRPORT,
        DESTINATION_AIRPORT,
        COUNT(*) AS FLIGHT_COUNT
    FROM flights_cleaned
    GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
    ORDER BY FLIGHT_COUNT DESC
    LIMIT 5
""").fetchall())