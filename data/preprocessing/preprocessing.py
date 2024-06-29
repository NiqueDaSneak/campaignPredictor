import pandas as pd
from sqlalchemy.orm import sessionmaker
from data.database import engine, RawCampaignData

# Set up the database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

def fetch_raw_data(session):
    """Fetch raw campaign data from the database."""
    raw_data = session.query(RawCampaignData).all()
    return raw_data

import pandas as pd

def preprocess_data(df):
    processed_data = []
    
    for index, row in df.iterrows():
        processed_data.append({
            'url': row.get('url', ''),
            'goal_amount': row.get('goal_amount', 0.0),
            'pledged_amount': row.get('pledged_amount', 0.0),
            'backers': row.get('backers', 0)
        })
    
    return pd.DataFrame(processed_data)

if __name__ == "__main__":
    raw_data = fetch_raw_data(session)
    preprocessed_data = preprocess_data(raw_data)
    
    # Save preprocessed data to CSV for later use
    preprocessed_data.to_csv('data/preprocessing/preprocessed_data.csv', index=False)
    
    session.close()
