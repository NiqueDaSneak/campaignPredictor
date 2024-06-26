import pandas as pd
from sklearn.metrics import mean_squared_error
import joblib

def evaluate_model(model, X_test, y_test):
    """Evaluate the model."""
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse

if __name__ == "__main__":
    # Load the testing data
    X_test = pd.read_csv('data/preprocessing/X_test.csv')
    y_test = pd.read_csv('data/preprocessing/y_test.csv')

    # Load the trained model from a file
    model = joblib.load('models/training/model.joblib')

    # Evaluate the model
    test_error = evaluate_model(model, X_test, y_test)
    print(f'Testing Error (MSE): {test_error}')
