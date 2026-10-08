# NEXUS: Data Dictionary & Architecture

## Core Relational Logic
Nexus is built on a 9-table PostgreSQL schema separating organizational hierarchy, project governance, and operational telemetry. 

### 1. Organizational & Project Governance
* **`offices` & `employees`:** Defines the population denominator. Active adoption cannot be measured by raw logins alone; it must be measured as `(Active Users / Total Employees per Office)`.
* **`transformation_projects` & `project_rollouts`:** Enables cohort analysis. Because the AI portal rolls out in phases (e.g., Boston as Pilot, London as Early Adopter), KPIs must be evaluated relative to the `rollout_start` date of each specific office, not a global average.

### 2. Operational Telemetry (The "Hands")
* **`employee_telemetry`:** Captures digital adoption. Event types include `LOGIN`, `SEARCH`, `AI_QUERY`, `SELF_SERVICE`, and `ESCALATE`. This isolates whether an employee successfully deflected a ticket via self-service or abandoned the portal.
* **`tickets` & `process_events`:** Reconstructs the ticket lifecycle. Instead of just a final state, `process_events` tracks every state change (e.g., `CREATED` → `AI_CLASSIFIED` → `AGENT_ASSIGNED`). This allows for precise calculation of Average Handling Time (AHT) and identification of routing bottlenecks.

### 3. Change Management Intelligence (The "Head & Heart")
* **`engagement_surveys`:** Houses qualitative feedback. The `sentiment_text` field acts as the raw input for the NLP layer to extract change resistance themes.
* **`intervention_actions`:** The closed-loop governance table. Records targeted actions taken when the system detects anomalies (e.g., triggering a "Local Manager Enablement" intervention in Singapore due to high escalation rates and low adoption).

## Scale & Dimensionality
The synthetic data pipeline generates realistic enterprise volumes:
* **Employees:** ~10,000 across 5 primary global hubs.
* **Telemetry:** 1M - 3M events simulating 6 months of rollout behavior.
* **Process Events:** 1M+ granular state changes representing 250,000 support tickets.