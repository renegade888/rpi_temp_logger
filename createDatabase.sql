CREATE TABLE sensor_data (
        sensor_id TEXT NOT NULL,
        timestamp datetime NOT NULL DEFAULT current_timestamp,
        value real NOT NULL
);
CREATE TABLE sensor (
        sensor_id TEXT NOT NULL UNIQUE,
        sensor_name   TEXT NOT NULL DEFAULT 'SensorName',
        PRIMARY KEY(sensor_id)
);
