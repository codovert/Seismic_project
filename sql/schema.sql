CREATE DATABASE IF NOT EXISTS seismic;
USE seismic;
DROP TABLE IF EXISTS earthquakes;
CREATE TABLE earthquakes (
  id VARCHAR(50) PRIMARY KEY, `time` DATETIME, updated DATETIME,
  latitude DOUBLE, longitude DOUBLE, depth_km DOUBLE, mag DOUBLE,
  magType VARCHAR(20), place VARCHAR(255), status VARCHAR(30),
  tsunami INT, sig INT, net VARCHAR(20), nst INT, dmin DOUBLE, rms DOUBLE,
  gap DOUBLE, magError DOUBLE, depthError DOUBLE, magNst INT,
  locationSource VARCHAR(20), magSource VARCHAR(20),
  types TEXT, ids TEXT, sources TEXT, `type` VARCHAR(50),
  country VARCHAR(100), continent VARCHAR(50),
  `year` INT, `month` INT, `day` INT, day_of_week VARCHAR(15), `hour` INT,
  depth_category VARCHAR(20), mag_category VARCHAR(20), is_strong TINYINT
);
