-- NEXUS: Global IT Helpdesk Transformation Schema
-- Database: PostgreSQL

CREATE TABLE offices (
    office_id VARCHAR(10) PRIMARY KEY,
    office_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(100),
    region VARCHAR(50),
    timezone VARCHAR(50),
    employee_count INT
);

CREATE TABLE employees (
    employee_id VARCHAR(20) PRIMARY KEY,
    office_id VARCHAR(10) REFERENCES offices(office_id),
    role_level VARCHAR(50),
    department VARCHAR(100),
    employment_type VARCHAR(50),
    join_date DATE,
    manager_id VARCHAR(20),
    change_cohort VARCHAR(50)
);

CREATE TABLE transformation_projects (
    project_id VARCHAR(20) PRIMARY KEY,
    project_name VARCHAR(200) NOT NULL,
    project_type VARCHAR(100),
    start_date DATE,
    target_end_date DATE,
    budget_usd DECIMAL(15,2),
    status VARCHAR(50),
    sponsor VARCHAR(100)
);

CREATE TABLE project_rollouts (
    rollout_id VARCHAR(20) PRIMARY KEY,
    project_id VARCHAR(20) REFERENCES transformation_projects(project_id),
    office_id VARCHAR(10) REFERENCES offices(office_id),
    phase VARCHAR(50),
    rollout_start DATE,
    rollout_end DATE,
    cohort VARCHAR(50),
    status VARCHAR(50)
);

CREATE TABLE employee_telemetry (
    event_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id),
    event_timestamp TIMESTAMP NOT NULL,
    session_id VARCHAR(50),
    event_type VARCHAR(50),
    feature VARCHAR(100),
    channel VARCHAR(50),
    duration_seconds INT,
    successful BOOLEAN
);

CREATE TABLE tickets (
    ticket_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id),
    office_id VARCHAR(10) REFERENCES offices(office_id),
    created_at TIMESTAMP NOT NULL,
    resolved_at TIMESTAMP,
    category VARCHAR(100),
    priority VARCHAR(20),
    channel VARCHAR(50),
    assigned_agent_id VARCHAR(20),
    resolution_type VARCHAR(50),
    csat_score INT
);

CREATE TABLE process_events (
    event_id VARCHAR(50) PRIMARY KEY,
    ticket_id VARCHAR(50) REFERENCES tickets(ticket_id),
    event_timestamp TIMESTAMP NOT NULL,
    event_type VARCHAR(50),
    actor_type VARCHAR(50),
    actor_id VARCHAR(50),
    queue VARCHAR(100),
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    duration_seconds INT
);

CREATE TABLE engagement_surveys (
    survey_id VARCHAR(50) PRIMARY KEY,
    employee_id VARCHAR(20) REFERENCES employees(employee_id),
    office_id VARCHAR(10) REFERENCES offices(office_id),
    survey_date DATE,
    survey_type VARCHAR(50),
    csat_score INT,
    sentiment_text TEXT
);

CREATE TABLE intervention_actions (
    intervention_id VARCHAR(50) PRIMARY KEY,
    office_id VARCHAR(10) REFERENCES offices(office_id),
    trigger_date DATE,
    signal_type VARCHAR(100),
    risk_level VARCHAR(20),
    recommended_action VARCHAR(200),
    action_owner VARCHAR(100),
    status VARCHAR(50),
    outcome_metric VARCHAR(100)
);

-- Indexing for high-volume telemetry and process analysis
CREATE INDEX idx_telemetry_emp ON employee_telemetry(employee_id);
CREATE INDEX idx_telemetry_time ON employee_telemetry(event_timestamp);
CREATE INDEX idx_process_ticket ON process_events(ticket_id);
CREATE INDEX idx_process_time ON process_events(event_timestamp);