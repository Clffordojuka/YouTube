Use weather;
SELECT * FROM weather_api;

# Filter cities by temp
SELECT City, Temperature
FROM weather_api
WHERE Temperature > 25;

# Group cities by weather description
SELECT Weather_Description, COUNT(*) AS City_Count
FROM weather_api
GROUP BY Weather_Description;

# Cities with extreme weather
SELECT City, Temperature, Humidity
FROM weather_api
WHERE Temperature > 30 OR Humidity < 30;

# Average wind speed by weather condition
SELECT Weather_Description, AVG(Wind_Speed) AS Avg_Wind_Speed
FROM weather_api
GROUP BY Weather_Description;

# Maximum and Minimum Temperature
SELECT MAX(Temperature) AS Max_Temperature, 
       MIN(Temperature) AS Min_Temperature
FROM weather_api;

# cities with overcast clouds
SELECT City, Cloudiness
FROM weather_api
WHERE Cloudiness = 100;

#Cities with high pressure
SELECT City, Pressure
FROM weather_api
WHERE Pressure >= 1012;

# Average temperature grouped by Wind speed Range
SELECT 
    CASE 
        WHEN Wind_Speed BETWEEN 0 AND 3 THEN '0-3 m/s'
        WHEN Wind_Speed BETWEEN 3 AND 6 THEN '3-6 m/s'
        ELSE '> 6 m/s'
    END AS Wind_Speed_Range,
    AVG(Temperature) AS Avg_Temperature
FROM weather_api
GROUP BY Wind_Speed_Range;

# Ranking cities by Temperature
SELECT 
    City, 
    Temperature,
    RANK() OVER (ORDER BY Temperature DESC) AS Temperature_Rank
FROM weather_api;

# Moving average of temperaure over cities
SELECT 
    City, 
    Temperature,
    ROUND(AVG(Temperature) OVER (ORDER BY Temperature ROWS BETWEEN 1 PRECEDING AND 1 FOLLOWING), 3) AS Moving_Avg_Temp
FROM weather_api;

# Cumulative sum of cloudiness
SELECT 
    City, 
    Cloudiness,
    SUM(Cloudiness) OVER (ORDER BY City) AS Cumulative_Cloudiness
FROM weather_api;

# Partitioning average temperature per weather description
SELECT 
    City, 
    Temperature,
    Weather_Description,
    ROUND(AVG(Temperature) OVER (PARTITION BY Weather_Description), 3) AS Avg_Temp_By_Weather
FROM weather_api;

# Rank citties by wind speed within weather categories
SELECT 
    City,
    Weather_Description,
    Wind_Speed,
    RANK() OVER (PARTITION BY Weather_Description ORDER BY Wind_Speed DESC) AS Wind_Speed_Rank
FROM weather_api;

# Find cities with the above average temperature by subquery
SELECT City, Temperature
FROM weather_api
WHERE Temperature > (SELECT AVG(Temperature) FROM weather_api);

#Get top ten Hottest cities using subquery
SELECT City, Temperature
FROM weather_api
WHERE Temperature IN (
    SELECT DISTINCT Temperature
    FROM (
        SELECT Temperature
        FROM weather_api
        ORDER BY Temperature DESC 
        LIMIT 10
    ) AS top_temperatures
);

#Find Cities with Maximum Temperature per Weather Description by subquery
SELECT City, Temperature, Weather_Description
FROM weather_api AS w1
WHERE Temperature = (
    SELECT MAX(Temperature)
    FROM weather_api AS w2
    WHERE w1.Weather_Description = w2.Weather_Description
);

#Use Partitioning to Rank Cities by Temperature within Weather Categories
SELECT 
    City, 
    Temperature,
    Weather_Description,
    DENSE_RANK() OVER (PARTITION BY Weather_Description ORDER BY Temperature DESC) AS Temp_Rank_By_Weather
FROM weather_api;

#Average Wind Speed Partitioned by City Groupings
SELECT 
    City,
    Wind_Speed,
    CASE
        WHEN Wind_Speed <= 3 THEN 'Low Wind'
        WHEN Wind_Speed BETWEEN 3 AND 6 THEN 'Medium Wind'
        ELSE 'High Wind'
    END AS Wind_Category,
    AVG(Wind_Speed) OVER (PARTITION BY 
        CASE 
            WHEN Wind_Speed <= 3 THEN 'Low Wind'
            WHEN Wind_Speed BETWEEN 3 AND 6 THEN 'Medium Wind'
            ELSE 'High Wind'
        END
    ) AS Avg_Wind_Speed_By_Category
FROM weather_api;

# Identify the Cities with Temperatures Above the Overall Average and Rank Them by Cloudiness
SELECT City, Temperature, Cloudiness, Cloudiness_Rank
FROM (
    SELECT 
        City,
        Temperature,
        Cloudiness,
        RANK() OVER (ORDER BY Cloudiness DESC) AS Cloudiness_Rank
    FROM weather_api
    WHERE Temperature > (SELECT AVG(Temperature) FROM weather_api)
) AS ranked_weather;
