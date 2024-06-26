import sys
import os
import pandas as pd
from data.scraping.kickstarter_scraper import scrape_kickstarter
from data.database import insert_raw_data, SessionLocal
from data.preprocessing.preprocessing import preprocess_data
from models.training.train_model import train_model
from predict.predict import load_model, make_predictions

def main(url):
    # Step 1: Scrape Kickstarter data
    print("Scraping Kickstarter data...")
    project_data = scrape_kickstarter(url)
    print("Data scraped:", project_data)

    # Step 2: Insert scraped data into the database
    print("Inserting data into the database...")
    session = SessionLocal()
    try:
        if not insert_raw_data(session, project_data):
            print(f"Data for URL {url} already exists in the database.")
            return
    finally:
        session.close()

    # Step 3: Preprocess the data
    print("Preprocessing data...")
    raw_data_df = pd.read_sql("SELECT * FROM raw_campaign_data", con=session.bind)
    processed_data_df = preprocess_data(raw_data_df)
    processed_data_df.to_sql("processed_campaign_data", con=session.bind, if_exists="replace", index=False)
    print("Data preprocessed and saved to the database.")

    # Step 4: Train the model
    print("Training model...")
    model = train_model(processed_data_df)
    model_path = "models/training/model.joblib"
    model.save(model_path)
    print(f"Model trained and saved to {model_path}")

    # Step 5: Make predictions
    print("Making predictions...")
    model = load_model(model_path)
    predictions = make_predictions(model, processed_data_df)
    print("Predictions:", predictions)

    # Optionally save predictions
    predictions_df = pd.DataFrame(predictions, columns=["Prediction"])
    predictions_df.to_csv("predictions.csv", index=False)
    print("Predictions saved to predictions.csv")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python pipeline.py <Kickstarter_URL>")
        sys.exit(1)

    url = sys.argv[1]
    main(url)
