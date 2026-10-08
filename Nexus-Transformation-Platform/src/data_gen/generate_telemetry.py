import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set random seeds for reproducibility
np.random.seed(42)

SIM_START = datetime(2026, 1, 1)
SIM_END = datetime(2026, 7, 1)
WEEKS = int((SIM_END - SIM_START).days / 7)

def generate_telemetry(employees_df):
    print(f"Generating 6 months of behavioral telemetry... (Simulating {WEEKS} weeks)")
    telemetry = []
    event_counter = 1

    # Loop through weeks to simulate the passage of time and adoption growth
    for week in range(WEEKS):
        # Base date for the week
        current_date = SIM_START + timedelta(days=week*7)
        month_index = week // 4  # Ranges from 0 (Jan) to 6 (July)

        for _, emp in employees_df.iterrows():
            office = emp['office_id']
            emp_id = emp['employee_id']

            # 1. THE NORMAL ADOPTION CURVE
            # Starts at 20%, grows by 12% each month, caps at 85%
            base_prob = min(0.20 + (month_index * 0.12), 0.85)
            success_rate = 0.75 # Normal AI self-service success

            # 2. THE SINGAPORE ANOMALY
            if office == "OFC-SIN":
                if month_index < 3: # Jan, Feb, Mar (Pre-Intervention)
                    base_prob = 0.30  # Stagnant low adoption
                    success_rate = 0.40 # High failure/escalation rate
                else:
                    # April onward (Post-Intervention)
                    base_prob = min(0.40 + ((month_index-3) * 0.20), 0.80)
                    success_rate = 0.70

            # 3. GENERATE EVENTS BASED ON PROBABILITY
            if np.random.rand() < base_prob:
                # Event 1: Employee logs into the AI Portal
                telemetry.append({
                    "event_id": f"EVT-{event_counter:07d}",
                    "employee_id": emp_id,
                    "event_timestamp": current_date + timedelta(days=np.random.randint(0, 5), hours=np.random.randint(8, 17)),
                    "session_id": f"SESS-{np.random.randint(10000, 99999)}",
                    "event_type": "LOGIN",
                    "feature": "AUTH",
                    "channel": "AI_PORTAL",
                    "duration_seconds": np.random.randint(10, 45),
                    "successful": True
                })
                event_counter += 1

                # Event 2: Does the AI resolve it, or do they escalate to a human?
                if np.random.rand() < success_rate:
                    end_event = "SELF_SERVICE"
                    feat = "KNOWLEDGE_ARTICLE"
                else:
                    end_event = "ESCALATE"
                    feat = "HUMAN_HANDOFF"

                telemetry.append({
                    "event_id": f"EVT-{event_counter:07d}",
                    "employee_id": emp_id,
                    "event_timestamp": current_date + timedelta(days=np.random.randint(0, 5), hours=np.random.randint(8, 17), minutes=np.random.randint(1, 10)),
                    "session_id": f"SESS-{np.random.randint(10000, 99999)}",
                    "event_type": end_event,
                    "feature": feat,
                    "channel": "AI_PORTAL",
                    "duration_seconds": np.random.randint(60, 300),
                    "successful": end_event == "SELF_SERVICE"
                })
                event_counter += 1

    return pd.DataFrame(telemetry)

if __name__ == "__main__":
    # Ensure raw data directory exists and load the employees
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    employees_path = os.path.join(output_dir, "employees.csv")
    
    if not os.path.exists(employees_path):
        print("Error: employees.csv not found. Run generate_employees.py first.")
        exit(1)
        
    employees_df = pd.read_csv(employees_path)
    
    # Generate the telemetry
    telemetry_df = generate_telemetry(employees_df)
    
    # Export to CSV
    telemetry_path = os.path.join(output_dir, "employee_telemetry.csv")
    telemetry_df.to_csv(telemetry_path, index=False)
    
    print(f"✅ Success! Saved {len(telemetry_df):,} telemetry events to data/raw/employee_telemetry.csv")