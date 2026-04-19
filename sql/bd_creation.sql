/* --- Creación de Base de Datos --- */

CREATE DATABASE scada_gateway_alarms GO
USE scada_gateway_alarms GO

/* --- Creación de Entidades --- */
CREATE TABLE alarm_severity (
    severity_id INT IDENTITY(1,1) PRIMARY KEY,
    severity_code VARCHAR(20) NOT NULL UNIQUE, -- LOW, MEDIUM, HIGH, CRITICAL
    severity_level INT NOT NULL,                -- 1,2,3,4
    description VARCHAR(100) NULL
);

CREATE TABLE source_system (
    source_system_id INT IDENTITY(1,1) PRIMARY KEY,
    system_name VARCHAR(50) NOT NULL UNIQUE,
    description VARCHAR(100) NULL
);

CREATE TABLE alarm_event (
    alarm_event_id BIGINT IDENTITY(1,1) PRIMARY KEY,

    tag VARCHAR(100) NOT NULL,
    description VARCHAR(255) NULL,

    severity_id INT NOT NULL,
    source_system_id INT NOT NULL,

    event_time DATETIME2(3) NOT NULL,
    cleared_time DATETIME2(3) NULL,

    status VARCHAR(20) NOT NULL, -- ACTIVE | CLEARED

    raw_payload_path NVARCHAR(MAX) NULL, -- JSON original opcional

    created_at DATETIME2(3) NOT NULL DEFAULT SYSUTCDATETIME(),

    CONSTRAINT FK_alarm_event_severity
        FOREIGN KEY (severity_id)
        REFERENCES alarm_severity(severity_id),

    CONSTRAINT FK_alarm_event_source
        FOREIGN KEY (source_system_id)
        REFERENCES source_system(source_system_id)
);

/* --- Creación de Indices --- */

CREATE INDEX IX_alarm_event_event_time
ON alarm_event (event_time);

CREATE INDEX IX_alarm_event_severity_time
ON alarm_event (severity_id, event_time);

CREATE INDEX IX_alarm_event_tag_time
ON alarm_event (tag, event_time);

CREATE INDEX IX_alarm_event_status_time
ON alarm_event (status, event_time);

/* --- Creación de Severidades ---- */

INSERT INTO alarm_severity (severity_code, severity_level)
VALUES 
('LOW', 1),
('MEDIUM', 2),
('HIGH', 3),
('CRITICAL', 4);