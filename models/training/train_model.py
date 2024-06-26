import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

def train_model(X_train, y_train):
    """Train the model."""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model

if __name__ == "__main__":
    # Load the training data
    X_train = pd.read_csv('data/preprocessing/X_train.csv')
    y_train = pd.read_csv('data/preprocessing/y_train.csv')

    # Train the model
    model = train_model(X_train, y_train)

    # Save the trained model to a file
    joblib.dump(model, 'models/training/model.joblib')

    # Optionally, you can print the training error
    y_train_pred = model.predict(X_train)
    train_error = mean_squared_error(y_train, y_train_pred)
    print(f'Training Error (MSE): {train_error}')
