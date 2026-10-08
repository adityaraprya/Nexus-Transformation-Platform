import pandas as pd
import numpy as np
import os

# --- FINANCIAL ASSUMPTIONS (From Phase 1 BRD) ---
BLENDED_HOURLY_RATE = 65.00
TRANSFORMATION_INVESTMENT = 2500000.00

def load_data():
    """Load the generated tickets dataset."""
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    tickets_path = os.path.join(raw_dir, "tickets.csv")
    
    if not os.path.exists(tickets_path):
        raise FileNotFoundError("tickets.csv not found. Please run data generators first.")
        
    df = pd.read_csv(tickets_path, parse_dates=['created_at', 'resolved_at'])
    return df

def run_roi_engine(df):
    """Calculates operational efficiencies and financial ROI."""
    
    # 1. Feature Engineering
    df['aht_minutes'] = (df['resolved_at'] - df['created_at']).dt.total_seconds() / 60.0
    df['month'] = df['created_at'].dt.month
    
    # 2. Identify Baseline (Jan/Feb) vs. Current Target State (June)
    baseline_df = df[df['month'].isin([1, 2])]
    current_df = df[df['month'] == 6]
    
    baseline_aht = baseline_df['aht_minutes'].mean()
    current_aht = current_df['aht_minutes'].mean()
    aht_reduction = baseline_aht - current_aht
    
    # 3. Analyze the Singapore Anomaly
    sin_baseline_aht = baseline_df[baseline_df['office_id'] == 'OFC-SIN']['aht_minutes'].mean()
    sin_current_aht = current_df[current_df['office_id'] == 'OFC-SIN']['aht_minutes'].mean()
    
    # 4. Financial Calculations
    # Projecting the June volume out for a full year
    monthly_volume = len(current_df)
    annualized_hours_saved = (aht_reduction * monthly_volume / 60) * 12
    annual_financial_benefit = annualized_hours_saved * BLENDED_HOURLY_RATE
    net_roi = ((annual_financial_benefit - TRANSFORMATION_INVESTMENT) / TRANSFORMATION_INVESTMENT) * 100

    # 5. Executive Summary Output
    print("\n" + "="*60)
    print(" 📊 NEXUS EXECUTIVE SUMMARY: TRANSFORMATION ROI")
    print("="*60)
    
    print("\n--- 1. OPERATIONAL EFFICIENCY ---")
    print(f"Global Baseline AHT (Q1):      {baseline_aht:.1f} minutes")
    print(f"Global Target AHT (June):      {current_aht:.1f} minutes")
    print(f"Net AHT Reduction:             ↓ {aht_reduction:.1f} minutes per ticket")
    
    print("\n--- 2. THE SINGAPORE RECOVERY ---")
    print(f"Singapore Pre-Intervention:    {sin_baseline_aht:.1f} minutes (Severe Friction)")
    print(f"Singapore Post-Intervention:   {sin_current_aht:.1f} minutes (Target Achieved)")
    
    print("\n--- 3. FINANCIAL IMPACT ---")
    print(f"Annualized Hours Saved:        {annualized_hours_saved:,.0f} hours")
    print(f"Labor Capacity Value:          ${annual_financial_benefit:,.2f}")
    print(f"Transformation Investment:     ${TRANSFORMATION_INVESTMENT:,.2f}")
    print("-" * 40)
    print(f"💰 ESTIMATED 12-MONTH ROI:      {net_roi:.1f}%")
    print("="*60 + "\n")

if __name__ == "__main__":
    print("Initializing Nexus ROI Engine...")
    tickets_df = load_data()
    run_roi_engine(tickets_df)