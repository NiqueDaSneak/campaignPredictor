import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(df, test_size=0.2):
    """Split the data into training and testing sets."""
    X = df.drop(columns=['url', 'pledged_amount'])  # Features
    y = df['pledged_amount']  # Target variable
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    # Load the preprocessed data
    df = pd.read_csv('data/preprocessing/preprocessed_data.csv')
    
    # Split the data
    X_train, X_test, y_train, y_test = split_data(df)
    
    # Save the splits to CSV files for later use
    X_train.to_csv('data/preprocessing/X_train.csv', index=False)
    X_test.to_csv('data/preprocessing/X_test.csv', index=False)
    y_train.to_csv('data/preprocessing/y_train.csv', index=False)
    y_test.to_csv('data/preprocessing/y_test.csv', index=False)
