import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

np.random.seed(42)
SIM_START = datetime(2026, 1, 1)
SIM_END = datetime(2026, 7, 1)
WEEKS = int((SIM_END - SIM_START).days / 7)

CATEGORIES = ["Hardware Request", "Software Access", "Password Reset", "Network Issue", "HR Portal"]
PRIORITIES = ["Low", "Medium", "High"]

def generate_tickets_and_events(employees_df):
    print("Generating IT Support Tickets and Process Events...")
    tickets = []
    process_events = []
    
    ticket_counter = 1
    event_counter = 1
    
    # We simulate about 500-1000 tickets per week across the globe
    for week in range(WEEKS):
        current_date = SIM_START + timedelta(days=week*7)
        month_index = week // 4 
        
        # Select a random subset of employees who submit a ticket this week (about 7%)
        weekly_submitters = employees_df.sample(frac=0.07)
        
        for _, emp in weekly_submitters.iterrows():
            office = emp['office_id']
            emp_id = emp['employee_id']
            
            # --- APPLY BUSINESS LOGIC (THE SINGAPORE ANOMALY) ---
            if office == "OFC-SIN" and month_index < 3:
                # Pre-intervention Singapore: High AHT, Low CSAT, High Human Escalation
                aht_minutes = int(np.random.normal(22, 5)) 
                csat = np.random.choice([1, 2, 3], p=[0.4, 0.4, 0.2])
                resolution = "HUMAN_ESCALATION"
                channel = "LEGACY_PORTAL"
            elif month_index < 3:
                # Pre-intervention Global: Average AHT, Average CSAT
                aht_minutes = int(np.random.normal(16, 4))
                csat = np.random.choice([3, 4, 5], p=[0.3, 0.5, 0.2])
                resolution = np.random.choice(["HUMAN_ESCALATION", "AI_DEFLECTION"], p=[0.7, 0.3])
                channel = np.random.choice(["LEGACY_PORTAL", "AI_PORTAL"], p=[0.6, 0.4])
            else:
                # Post-intervention (Target State achieved globally)
                aht_minutes = int(np.random.normal(11, 3))
                csat = np.random.choice([4, 5], p=[0.6, 0.4])
                resolution = np.random.choice(["HUMAN_ESCALATION", "AI_DEFLECTION"], p=[0.3, 0.7])
                channel = "AI_PORTAL"
                
            # Ensure AHT doesn't go below 2 mins
            aht_minutes = max(2, aht_minutes)
            
            # Create Ticket Timestamps
            created_at = current_date + timedelta(days=np.random.randint(0, 5), hours=np.random.randint(8, 16))
            resolved_at = created_at + timedelta(minutes=aht_minutes)
            
            ticket_id = f"TKT-{ticket_counter:06d}"
            
            # 1. GENERATE THE TICKET RECORD
            tickets.append({
                "ticket_id": ticket_id,
                "employee_id": emp_id,
                "office_id": office,
                "created_at": created_at,
                "resolved_at": resolved_at,
                "category": np.random.choice(CATEGORIES),
                "priority": np.random.choice(PRIORITIES, p=[0.6, 0.3, 0.1]),
                "channel": channel,
                "assigned_agent_id": f"AGT-{np.random.randint(100, 150)}" if resolution == "HUMAN_ESCALATION" else "AI_SYS",
                "resolution_type": resolution,
                "csat_score": csat
            })
            
            # 2. GENERATE THE GRANULAR PROCESS EVENTS
            # Event: CREATED
            process_events.append({
                "event_id": f"PE-{event_counter:08d}",
                "ticket_id": ticket_id,
                "event_timestamp": created_at,
                "event_type": "CREATED",
                "actor_type": "EMPLOYEE",
                "actor_id": emp_id,
                "duration_seconds": 0
            })
            event_counter += 1
            
            # Event: AI_CLASSIFIED (Happens 1 min later)
            class_time = created_at + timedelta(minutes=1)
            process_events.append({
                "event_id": f"PE-{event_counter:08d}",
                "ticket_id": ticket_id,
                "event_timestamp": class_time,
                "event_type": "AI_CLASSIFIED",
                "actor_type": "SYSTEM",
                "actor_id": "AI_ENGINE",
                "duration_seconds": 60
            })
            event_counter += 1
            
            # Event: RESOLVED
            process_events.append({
                "event_id": f"PE-{event_counter:08d}",
                "ticket_id": ticket_id,
                "event_timestamp": resolved_at,
                "event_type": "RESOLVED",
                "actor_type": "AGENT" if resolution == "HUMAN_ESCALATION" else "SYSTEM",
                "actor_id": f"AGT-{np.random.randint(100, 150)}" if resolution == "HUMAN_ESCALATION" else "AI_ENGINE",
                "duration_seconds": (aht_minutes - 1) * 60
            })
            event_counter += 1
            ticket_counter += 1

    return pd.DataFrame(tickets), pd.DataFrame(process_events)

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    employees_path = os.path.join(output_dir, "employees.csv")
    
    if not os.path.exists(employees_path):
        print("Error: employees.csv not found.")
        exit(1)
        
    employees_df = pd.read_csv(employees_path)
    tickets_df, events_df = generate_tickets_and_events(employees_df)
    
    tickets_df.to_csv(os.path.join(output_dir, "tickets.csv"), index=False)
    events_df.to_csv(os.path.join(output_dir, "process_events.csv"), index=False)
    
    print(f"✅ Success! Saved {len(tickets_df):,} tickets and {len(events_df):,} process events to data/raw/")