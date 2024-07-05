import pandas as pd

def preprocess_data(df):
    processed_data = []

    for index, row in df.iterrows():
        processed_data.append({
            'url': row.get('url', ''),
            'goal_amount': row.get('goal_amount', 0.0),
            'pledged_amount': row.get('pledged_amount', 0.0),
            'backers': row.get('backers', 0),
            'story_content': row.get('story_content', '')
        })
    
    return pd.DataFrame(processed_data)

if __name__ == "__main__":
    raw_data = pd.read_json("data/preprocessing/raw_data.json")
    preprocessed_data = preprocess_data(raw_data)
    preprocessed_data.to_csv("data/preprocessing/preprocessed_data.csv", index=False)
