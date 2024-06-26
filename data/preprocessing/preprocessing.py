import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://dbuser:password@localhost/mydatabase')

def process_data():
    raw_data = pd.read_sql_table('raw_campaign_data', engine)
    processed_data = raw_data.copy()
    
    # Example processing: adding a success_rate column
    processed_data['success_rate'] = processed_data['pledged_amount'] / processed_data['goal_amount']
    
    processed_data.to_sql('processed_campaign_data', engine, if_exists='replace', index=False)

if __name__ == "__main__":
    process_data()
