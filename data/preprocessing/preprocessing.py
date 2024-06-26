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

def preprocess_data(raw_data_df):
    # Example preprocessing steps
    processed_data = []

    for index, row in raw_data_df.iterrows():
        processed_data.append({
            'url': row['url'],
            'goal_amount': row['goal_amount'],
            'pledged_amount': row['pledged_amount'],
            'backers': row['backers'],
            'feature_1': row['goal_amount'] / row['backers'] if row['backers'] > 0 else 0,
            'feature_2': row['pledged_amount'] / row['goal_amount'] if row['goal_amount'] > 0 else 0
        })

    processed_data_df = pd.DataFrame(processed_data)
    return processed_data_df

if __name__ == "__main__":
    raw_data = fetch_raw_data(session)
    preprocessed_data = preprocess_data(raw_data)
    
    # Save preprocessed data to CSV for later use
    preprocessed_data.to_csv('data/preprocessing/preprocessed_data.csv', index=False)
    
    session.close()
