import joblib
from sqlalchemy import create_engine
import pandas as pd
from sklearn.linear_model import LinearRegression

engine = create_engine('postgresql://dbuser:password@localhost/mydatabase')

def train_model():
    processed_data = pd.read_sql_table('processed_campaign_data', engine)
    
    # Example: training a simple linear regression model
    model = LinearRegression()
    model.fit(processed_data[['goal_amount', 'backers']], processed_data['pledged_amount'])
    
    # Save the model to a binary string
    model_blob = joblib.dumps(model)
    
    # Insert the model into the database
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO trained_models (model_type, model_blob)
        VALUES (%s, %s)
    """, ('Linear Regression', model_blob))
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    train_model()
