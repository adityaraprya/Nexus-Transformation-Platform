# Nexus Simulation Configuration

NUM_EMPLOYEES = 10000
SIMULATION_START = "2026-01-01"
SIMULATION_END = "2026-07-01"

# Office definitions and population weights
OFFICES = {
    "OFC-BOS": {"name": "Boston", "country": "USA", "region": "NAMR", "weight": 0.25},
    "OFC-NYC": {"name": "New York", "country": "USA", "region": "NAMR", "weight": 0.20},
    "OFC-LON": {"name": "London", "country": "UK", "region": "EMEA", "weight": 0.20},
    "OFC-GUR": {"name": "Gurgaon", "country": "India", "region": "APAC", "weight": 0.20},
    "OFC-SIN": {"name": "Singapore", "country": "Singapore", "region": "APAC", "weight": 0.15},
}

DEPARTMENTS = ["Consulting", "Digital Ventures", "Operations", "Finance", "HR", "IT"]

# Hierarchical roles mapped to rough corporate distribution
ROLES = {
    "Analyst": 0.35,
    "Consultant": 0.30,
    "Project Leader": 0.15,
    "Principal": 0.10,
    "Partner": 0.07,
    "Managing Director": 0.03
}