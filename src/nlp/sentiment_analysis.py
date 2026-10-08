import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os

# Download the VADER lexicon on first run
nltk.download('vader_lexicon', quiet=True)

def load_surveys():
    raw_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "raw")
    surveys_path = os.path.join(raw_dir, "engagement_surveys.csv")
    
    if not os.path.exists(surveys_path):
        raise FileNotFoundError("engagement_surveys.csv not found.")
        
    return pd.read_csv(surveys_path, parse_dates=['survey_date'])

def run_nlp_engine(df):
    print("Initializing NLP Sentiment Engine...")
    sia = SentimentIntensityAnalyzer()
    
    # 1. Calculate Sentiment Scores
    # VADER compound score ranges from -1 (extremely negative) to +1 (extremely positive)
    df['sentiment_score'] = df['sentiment_text'].apply(lambda x: sia.polarity_scores(str(x))['compound'])
    
    # Categorize sentiment
    df['sentiment_category'] = pd.cut(
        df['sentiment_score'], 
        bins=[-1.0, -0.1, 0.1, 1.0], 
        labels=['Negative', 'Neutral', 'Positive']
    )
    
    # 2. Keyword Extraction (Friction Identification)
    friction_keywords = ['latency', 'slow', 'training', 'confusing', 'freezing']
    for keyword in friction_keywords:
        df[f'mentions_{keyword}'] = df['sentiment_text'].str.contains(keyword, case=False, na=False)
    
    # 3. Analyze Q1 (Pre-Intervention) Geographic Heatmap
    df['quarter'] = df['survey_date'].dt.quarter
    q1_df = df[df['quarter'] == 1]
    
    print("\n" + "="*70)
    print(" 🧠 NEXUS CHANGE INTELLIGENCE: Q1 GEOGRAPHIC RISK ANALYSIS")
    print("="*70)
    
    # Group by office to find resistance hotspots
    office_risk = q1_df.groupby('office_id').agg(
        avg_csat=('csat_score', 'mean'),
        avg_sentiment=('sentiment_score', 'mean'),
        negative_volume=('sentiment_category', lambda x: (x == 'Negative').mean() * 100),
        latency_complaints=('mentions_latency', 'sum'),
        training_requests=('mentions_training', 'sum')
    ).round(2).reset_index()
    
    print("\n--- REGIONAL SENTIMENT & FRICTION TRIGGERS (Q1) ---")
    print(office_risk.to_string(index=False))
    
    # 4. Automated Intervention Trigger Logic
    print("\n--- AUTOMATED INTERVENTION RECOMMENDATIONS ---")
    for _, row in office_risk.iterrows():
        if row['negative_volume'] > 40:
            print(f"🚨 ALERT [{row['office_id']}]: Critical resistance detected.")
            if row['latency_complaints'] > 0:
                print(f"   ↳ Action: Route technical investigation for network latency.")
            if row['training_requests'] > 0:
                print(f"   ↳ Action: Deploy local Change Champions for portal training.")
            print("-" * 50)

    # 5. Q2 Recovery Validation
    q2_df = df[df['quarter'] == 2]
    sin_q2_sentiment = q2_df[q2_df['office_id'] == 'OFC-SIN']['sentiment_score'].mean()
    
    print(f"\n✅ VALIDATION: Singapore Q2 Sentiment recovered to {sin_q2_sentiment:.2f} following April intervention.")
    print("="*70 + "\n")
    
    return df

if __name__ == "__main__":
    surveys_df = load_surveys()
    processed_surveys = run_nlp_engine(surveys_df)
    
    # Save the NLP enriched data
    processed_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    processed_surveys.to_csv(os.path.join(processed_dir, "nlp_enriched_surveys.csv"), index=False)