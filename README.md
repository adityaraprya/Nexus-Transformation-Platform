# NEXUS: Global IT Helpdesk Transformation & Change Intelligence Platform

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-green.svg)
![NLP](https://img.shields.io/badge/NLP-VADER_Sentiment-orange.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Executive_Dashboard-red.svg)

## 📌 Executive Summary
Global organizations invest heavily in digital transformation (e.g., AI enablement), yet frequently fail to realize projected ROI due to a disconnect between operational deployment and human change management. 

**Nexus** is an end-to-end operational intelligence portfolio project that bridges this gap. It simulates the rollout of an AI-enabled IT Helpdesk across 10,000 global employees, tracking digital adoption, quantifying employee sentiment via NLP, and proving the financial ROI of targeted change-management interventions.

## 📊 Business Impact & Simulated Outcomes
* **Transformation ROI:** 68%
* **Annualized Hours Saved:** ~56,000 hours (Labor capacity released)
* **Average Handling Time (AHT) Reduction:** Dropped from 18.0 mins to 11.0 mins globally.
* **Change Intelligence:** Successfully detected and resolved the "Singapore Anomaly"—a Q1 adoption failure driven by platform latency, identified entirely through automated NLP sentiment extraction.

## 🏗️ System Architecture & Methodology

### 1. Data Engineering & Relational Design (`/database`, `/src/data_gen`)
* Designed a 9-table PostgreSQL schema separating organizational hierarchy from operational telemetry.
* Engineered a Python-based synthetic data generator producing ~1,000,000+ rows of telemetry, tickets, and process events.
* **Key Differentiator:** The synthetic data is not random; it contains mathematically embedded business logic, S-curve adoption models, and regional behavioral anomalies.

### 2. NLP Change Intelligence Engine (`/src/nlp`)
* Ingests unstructured employee engagement surveys.
* Utilizes **NLTK (VADER)** to score text sentiment and categorize friction triggers (e.g., "latency", "training").
* Acts as an automated early-warning system for the Operating Committee to deploy local interventions before ROI degrades.

### 3. Executive Dashboard (`/dashboards`)
* A fully interactive **Streamlit** web application designed for an Operating Committee.
* Synthesizes millions of granular data points into top-line metrics (ROI, AHT, Regional THS).

## 🚀 How to Run Locally

**1. Clone the repository and install dependencies:**
```bash
git clone [https://github.com/adityaraprya/Nexus-Transformation-Platform.git](https://github.com/adityaraprya/Nexus-Transformation-Platform.git)
cd Nexus-Transformation-Platform
pip install pandas numpy faker nltk streamlit plotly
📂 Repository Structure
Nexus-Transformation-Platform/
├── dashboards/
│   └── app.py                          # Streamlit UI
├── data/
│   ├── processed/                      # NLP enriched data
│   └── raw/                            # Generated operational data
├── database/
│   └── schema.sql                      # 9-table PostgreSQL relational model
├── docs/
│   ├── phase-1-strategy/
│   │   └── 01-business-requirements.md # Strategic Blueprint & KPIs
│   └── phase-2-data/
│       └── 02-data-dictionary.md       # Data Contract
└── src/
    ├── analytics/
    │   └── operational_kpis.py         # Financial ROI engine
    ├── data_gen/
    │   ├── config.py                   # Business logic parameters
    │   ├── generate_employees.py       
    │   ├── generate_surveys.py
    │   ├── generate_telemetry.py
    │   └── generate_tickets.py
    └── nlp/
        └── sentiment_analysis.py       # VADER unstructured text engine
