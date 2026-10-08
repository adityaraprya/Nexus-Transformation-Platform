import pandas as pd
import numpy as np
from faker import Faker
import os
import config

fake = Faker()
Faker.seed(42)
np.random.seed(42)

def generate_offices():
    """Generates the static offices table."""
    print("Generating office locations...")
    offices_data = []
    
    for office_id, data in config.OFFICES.items():
        offices_data.append({
            "office_id": office_id,
            "office_name": data["name"],
            "city": data["name"],
            "country": data["country"],
            "region": data["region"],
            "timezone": fake.timezone(),
            "employee_count": int(config.NUM_EMPLOYEES * data["weight"])
        })
        
    return pd.DataFrame(offices_data)

def generate_employees(offices_df):
    """Generates the employee population distributed across offices."""
    print(f"Generating {config.NUM_EMPLOYEES} employee profiles...")
    employees = []
    
    # Extract office IDs and their exact population weights
    office_ids = offices_df['office_id'].tolist()
    weights = [config.OFFICES[oid]["weight"] for oid in office_ids]
    
    # Assign offices and roles based on probability distributions
    assigned_offices = np.random.choice(office_ids, size=config.NUM_EMPLOYEES, p=weights)
    roles = list(config.ROLES.keys())
    role_probs = list(config.ROLES.values())
    
    for i in range(config.NUM_EMPLOYEES):
        employees.append({
            "employee_id": f"EMP-{i+1000:05d}",
            "office_id": assigned_offices[i],
            "role_level": np.random.choice(roles, p=role_probs),
            "department": np.random.choice(config.DEPARTMENTS),
            "employment_type": "Full-Time",
            "join_date": fake.date_between(start_date='-5y', end_date='today').strftime('%Y-%m-%d'),
            "change_cohort": "Target Population"
        })
        
    return pd.DataFrame(employees)

if __name__ == "__main__":
    offices_df = generate_offices()
    employees_df = generate_employees(offices_df)
    
    # Ensure raw data directory exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    os.makedirs(output_dir, exist_ok=True)
    
    # Export to CSV
    offices_df.to_csv(os.path.join(output_dir, "offices.csv"), index=False)
    employees_df.to_csv(os.path.join(output_dir, "employees.csv"), index=False)
    
    print(f"✅ Success! Saved {len(offices_df)} offices and {len(employees_df)} employees to data/raw/")