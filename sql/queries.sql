-- 1. Top 10 strongest earthquakes
SELECT id, place, country, mag, `time` FROM earthquakes ORDER BY mag DESC LIMIT 10;

-- 2. Top 10 deepest earthquakes
SELECT id, place, country, depth_km, mag FROM earthquakes ORDER BY depth_km DESC LIMIT 10;

-- 3. Shallow earthquakes (<50 km) with magnitude > 7.5
SELECT id, place, country, depth_km, mag, `time` FROM earthquakes
WHERE depth_km < 50 AND mag > 7.5 ORDER BY mag DESC;

-- 5. Average magnitude per magnitude type
SELECT magType, ROUND(AVG(mag),2) AS avg_mag, COUNT(*) AS events FROM earthquakes
GROUP BY magType ORDER BY avg_mag DESC;

-- 6. Year with the most earthquakes
SELECT `year`, COUNT(*) AS total FROM earthquakes GROUP BY `year` ORDER BY total DESC;

-- 7. Month with the highest number of earthquakes
SELECT `month`, COUNT(*) AS total FROM earthquakes GROUP BY `month` ORDER BY total DESC;

-- 8. Day of week with the most earthquakes
SELECT day_of_week, COUNT(*) AS total FROM earthquakes GROUP BY day_of_week ORDER BY total DESC;

-- 9. Earthquakes per hour of day
SELECT `hour`, COUNT(*) AS total FROM earthquakes GROUP BY `hour` ORDER BY `hour`;

-- 10. Most active reporting network
SELECT net, COUNT(*) AS total FROM earthquakes GROUP BY net ORDER BY total DESC;

-- 11. Top 5 countries by total significance (casualty proxy)
SELECT country, SUM(sig) AS total_significance, COUNT(*) AS events FROM earthquakes
GROUP BY country ORDER BY total_significance DESC LIMIT 5;

-- 13. Average significance by magnitude category (alert-level proxy)
SELECT mag_category, ROUND(AVG(sig),1) AS avg_significance, COUNT(*) AS events FROM earthquakes
GROUP BY mag_category ORDER BY avg_significance DESC;

-- 20. Count of earthquakes by magnitude category (alert-level proxy)
SELECT mag_category, COUNT(*) AS total FROM earthquakes
GROUP BY mag_category ORDER BY total DESC;

-- 14. Reviewed vs automatic earthquakes
SELECT status, COUNT(*) AS total FROM earthquakes GROUP BY status;

-- 15. Count by earthquake type
SELECT `type`, COUNT(*) AS total FROM earthquakes GROUP BY `type` ORDER BY total DESC;

-- 16. Number of earthquakes by data type
SELECT types, COUNT(*) AS total FROM earthquakes GROUP BY types ORDER BY total DESC LIMIT 20;

-- 18. Events with high station coverage (nst > 100)
SELECT id, place, country, nst, mag FROM earthquakes WHERE nst > 100 ORDER BY nst DESC LIMIT 100;

-- 19. Tsunamis triggered per year
SELECT `year`, SUM(tsunami) AS tsunami_events FROM earthquakes GROUP BY `year` ORDER BY `year`;

-- 21. Top 5 countries by average magnitude (min 30 events)
SELECT country, ROUND(AVG(mag),2) AS avg_mag, COUNT(*) AS events FROM earthquakes
WHERE continent <> 'Ocean/Other'
GROUP BY country HAVING COUNT(*) >= 30 ORDER BY avg_mag DESC LIMIT 5;

-- 22. Countries with both shallow and deep earthquakes in the same month
SELECT country, `year`, `month` FROM earthquakes
GROUP BY country, `year`, `month`
HAVING SUM(depth_category='Shallow') > 0 AND SUM(depth_category='Deep') > 0
ORDER BY `year`, `month`;

-- 23. Year-over-year growth in earthquakes
WITH yearly AS (SELECT `year` AS yr, COUNT(*) AS cnt FROM earthquakes GROUP BY `year`)
SELECT yr, cnt, LAG(cnt) OVER (ORDER BY yr) AS prev_year,
       ROUND((cnt - LAG(cnt) OVER (ORDER BY yr)) * 100 / LAG(cnt) OVER (ORDER BY yr), 2) AS growth_pct
FROM yearly ORDER BY yr;

-- 24. Top 3 most active regions (frequency x average magnitude)
SELECT country, COUNT(*) AS events, ROUND(AVG(mag),2) AS avg_mag,
       ROUND(COUNT(*) * AVG(mag), 1) AS activity_score
FROM earthquakes GROUP BY country ORDER BY activity_score DESC LIMIT 3;

-- 25. Average depth per country within ±5° of the equator
SELECT country, ROUND(AVG(depth_km),2) AS avg_depth_km, COUNT(*) AS events FROM earthquakes
WHERE latitude BETWEEN -5 AND 5 AND continent <> 'Ocean/Other'
GROUP BY country ORDER BY avg_depth_km DESC;

-- 26. Countries with the highest shallow-to-deep ratio (min 30 events)
SELECT country, SUM(depth_category='Shallow') AS shallow, SUM(depth_category='Deep') AS deep,
       ROUND(SUM(depth_category='Shallow') / NULLIF(SUM(depth_category='Deep'),0), 2) AS ratio
FROM earthquakes WHERE continent <> 'Ocean/Other'
GROUP BY country HAVING COUNT(*) >= 30 AND deep > 0
ORDER BY ratio DESC LIMIT 15;

-- 27. Average magnitude difference: tsunami vs no tsunami
SELECT ROUND(AVG(CASE WHEN tsunami=1 THEN mag END),3) AS avg_mag_tsunami,
       ROUND(AVG(CASE WHEN tsunami=0 THEN mag END),3) AS avg_mag_no_tsunami,
       ROUND(AVG(CASE WHEN tsunami=1 THEN mag END) - AVG(CASE WHEN tsunami=0 THEN mag END),3) AS difference
FROM earthquakes;

-- 28. Events with the lowest data reliability (gap + rms)
SELECT id, place, gap, rms,
       ROUND(gap / (SELECT MAX(gap) FROM earthquakes) + rms / (SELECT MAX(rms) FROM earthquakes), 3) AS unreliability_score
FROM earthquakes ORDER BY unreliability_score DESC LIMIT 20;

-- 30. Regions with the most deep-focus earthquakes (> 300 km)
SELECT country, COUNT(*) AS deep_events, ROUND(AVG(depth_km),1) AS avg_depth FROM earthquakes
WHERE depth_km > 300 GROUP BY country ORDER BY deep_events DESC LIMIT 15;
