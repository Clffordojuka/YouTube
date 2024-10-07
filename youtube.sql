create database youtube;
 SHOW DATABASES;
select * from youtube_videos
 
 SELECT * FROM youtube_videos
 WHERE title = 'Citizen Tv Kenya';
 
 #Using the wildcard "LIKE"
 SELECT * FROM youtube_videos
WHERE channel_id LIKE '%Q';

 SELECT * FROM youtube_videos
WHERE title LIKE '%kenya%';

#Working with aggregates (Count)
SELECT title, count(*) AS video_count
FROM youtube_videos
GROUP BY title; 

#working with average
SELECT avg(subscribers) AS Average_subscribers
FROM youtube_videos;

#working Max and Min
SELECT title, MAX(total_views) AS max_views, MIN(total_views) AS min_views
FROM youtube_videos
GROUP BY title;

#working with sum
SELECT title, SUM(total_views) AS total_views
FROM youtube_videos
GROUP BY title;

#working aggregates together with operators
SELECT COUNT(*) AS channels_with_many_subscribers
FROM youtube_videos
WHERE subscribers > 10000;

#Combination of aggregate function
SELECT title,
       COUNT(*) AS video_count,
       AVG(subscribers) AS average_subscribers,
       SUM(total_views) AS total_views
FROM youtube_videos
GROUP BY title;

#Top 5 channels by the total views
SELECT title, SUM(total_views) AS total_views
FROM youtube_videos
GROUP BY title
ORDER BY total_views DESC
LIMIT 5;

#Top 5 channels with most videos
SELECT title, COUNT(*) AS video_count
FROM youtube_videos
GROUP BY title
ORDER BY video_count DESC
LIMIT 5;

#Working with case statement
SELECT 
    CASE 
        WHEN subscribers < 1000 THEN '0-1000'
        WHEN subscribers BETWEEN 1000 AND 9999 THEN '1000-9999'
        WHEN subscribers BETWEEN 10000 AND 99999 THEN '10000-99999'
        ELSE '100000+'
    END AS subscriber_range,
    COUNT(*) AS channel_count
FROM youtube_videos
GROUP BY subscriber_range;

#Subquery at the select clause
SELECT title, 
       total_views,
       (SELECT AVG(total_views) FROM youtube_videos) AS average_views
FROM youtube_videos;

#Subsequeries at the where clause
SELECT title, total_views
FROM youtube_videos
WHERE total_views > (SELECT AVG(total_views) FROM youtube_videos);

#Window functions with ROW_NUMBER()
SELECT title,
       total_views,
       ROW_NUMBER() OVER (ORDER BY total_views DESC) AS RANKk
FROM youtube_videos;

#window functions with RANK()
SELECT title,
       total_views,
       RANK() OVER (ORDER BY total_views DESC) AS Rankz
FROM youtube_videos;

#Combination of subqueries and Window function alongside WITH function
WITH RankedChannels AS (
    SELECT title,
           total_views,
           AVG(total_views) OVER () AS average_views,
           RANK() OVER (ORDER BY total_views DESC) AS rankx
    FROM youtube_videos
)
SELECT title, total_views, rankx
FROM RankedChannels
WHERE total_views > average_views;

#Views growth per month (Time_based analysis)
SELECT DATE_FORMAT(published_at, '%Y-%m') AS month, 
       SUM(total_views) AS total_views_per_month
FROM youtube_videos
GROUP BY month
ORDER BY month;
