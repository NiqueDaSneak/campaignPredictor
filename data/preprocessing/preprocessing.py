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

def preprocess_data(raw_data):
    """Clean and transform the raw data."""
    data = [{
        'url': d.url,
        'goal_amount': d.goal_amount,
        'pledged_amount': d.pledged_amount,
        'backers': d.backers
    } for d in raw_data]

    df = pd.DataFrame(data)
    
    # Example preprocessing steps:
    # 1. Handle missing values
    df.fillna(0, inplace=True)
    
    # 2. Feature engineering (if needed)
    df['success_rate'] = df['pledged_amount'] / df['goal_amount']
    
    return df

if __name__ == "__main__":
    raw_data = fetch_raw_data(session)
    preprocessed_data = preprocess_data(raw_data)
    
    # Save preprocessed data to CSV for later use
    preprocessed_data.to_csv('data/preprocessing/preprocessed_data.csv', index=False)
    
    session.close()
