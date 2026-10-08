import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import random

np.random.seed(42)
random.seed(42)

SIM_START = datetime(2026, 1, 1)
SIM_END = datetime(2026, 7, 1)
WEEKS = int((SIM_END - SIM_START).days / 7)

# Qualitative Feedback Templates
POSITIVE_FEEDBACK = [
    "The new AI system is incredibly fast. Saves me a lot of time.",
    "Very intuitive workflow, much better than the legacy portal.",
    "Self-service articles were actually helpful for once.",
    "Great experience. The AI resolved my password issue in seconds.",
    "Smooth transition. No complaints."
]

NEUTRAL_FEEDBACK = [
    "It's okay. Takes some getting used to.",
    "Standard IT portal. Nothing special.",
    "Worked fine, but I prefer emailing a real person.",
    "AI is decent, but didn't fully understand my specific network issue."
]

NEGATIVE_FRICTION = [
    "System is way too slow. Massive latency when loading the dashboard.",
    "I don't know how to use this. We need more training on the AI portal.",
    "Keeps freezing. The latency makes it unusable.",
    "Stop forcing us to use the AI. It's too slow and I need human help.",
    "Confusing interface. I just want to submit an email ticket."
]

def generate_surveys(employees_df):
    print("Generating qualitative engagement surveys...")
    surveys = []
    survey_counter = 1
    
    for week in range(WEEKS):
        current_date = SIM_START + timedelta(days=week*7)
        month_index = week // 4
        
        # 3% of employees fill out a survey each week
        weekly_submitters = employees_df.sample(frac=0.03)
        
        for _, emp in weekly_submitters.iterrows():
            office = emp['office_id']
            emp_id = emp['employee_id']
            
            # --- THE SINGAPORE ANOMALY LOGIC ---
            if office == "OFC-SIN" and month_index < 3:
                # Pre-intervention Singapore: High friction, low CSAT
                csat = np.random.choice([1, 2, 3], p=[0.5, 0.3, 0.2])
                text = random.choice(NEGATIVE_FRICTION)
            elif month_index < 3:
                # Pre-intervention Global: Normal distribution
                csat = np.random.choice([3, 4, 5], p=[0.2, 0.5, 0.3])
                if csat >= 4: text = random.choice(POSITIVE_FEEDBACK)
                elif csat == 3: text = random.choice(NEUTRAL_FEEDBACK)
                else: text = random.choice(NEGATIVE_FRICTION)
            else:
                # Post-intervention (Global Stabilization)
                csat = np.random.choice([4, 5], p=[0.5, 0.5])
                text = random.choice(POSITIVE_FEEDBACK)
                
            surveys.append({
                "survey_id": f"SRV-{survey_counter:06d}",
                "employee_id": emp_id,
                "office_id": office,
                "survey_date": current_date.strftime('%Y-%m-%d'),
                "survey_type": "POST_RESOLUTION",
                "csat_score": csat,
                "sentiment_text": text
            })
            survey_counter += 1
            
    return pd.DataFrame(surveys)

if __name__ == "__main__":
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    employees_path = os.path.join(output_dir, "employees.csv")
    
    if not os.path.exists(employees_path):
        print("Error: employees.csv not found.")
        exit(1)
        
    employees_df = pd.read_csv(employees_path)
    surveys_df = generate_surveys(employees_df)
    
    surveys_df.to_csv(os.path.join(output_dir, "engagement_surveys.csv"), index=False)
    print(f"✅ Success! Saved {len(surveys_df):,} employee surveys to data/raw/engagement_surveys.csv")