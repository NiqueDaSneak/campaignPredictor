import pandas as pd
from sklearn.model_selection import train_test_split

def split_data(df):
    X = df.drop(columns=['amount_raised'])
    y = df['amount_raised']
    return train_test_split(X, y, test_size=0.2, random_state=42)

# Example usage
if __name__ == "__main__":
    df = pd.read_sql('SELECT * FROM campaigns', engine)
    X_train, X_test, y_train, y_test = split_data(df)
