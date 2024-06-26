import joblib
from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('postgresql://dbuser:password@localhost/mydatabase')

def predict(campaign_details):
    # Load the trained model from the database
    conn = engine.raw_connection()
    cur = conn.cursor()
    cur.execute("SELECT model_blob FROM trained_models ORDER BY training_date DESC LIMIT 1")
    model_blob = cur.fetchone()[0]
    cur.close()
    conn.close()
    
    model = joblib.loads(model_blob)
    
    # Predict using the model
    prediction = model.predict([[
        campaign_details['goal_amount'],
        campaign_details['backers']
    ]])
    
    return prediction[0]

if __name__ == "__main__":
    campaign_details = {
        'goal_amount': 5000,
        'backers': 100
    }
    prediction = predict(campaign_details)
    print(f"Predicted amount raised: {prediction}")
