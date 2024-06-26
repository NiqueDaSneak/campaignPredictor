import joblib
from sklearn.metrics import mean_squared_error
from data_preprocessing.preprocess import preprocess_data
from data_preprocessing.train_test_split import split_data

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    return mse

# Example usage
if __name__ == "__main__":
    df = pd.read_sql('SELECT * FROM campaigns', engine)
    X_train, X_test, y_train, y_test = split_data(df)
    X_test = preprocess_data(X_test)
    model = joblib.load('../models/model.joblib')
    mse = evaluate_model(model, X_test, y_test)
    print(f'Mean Squared Error: {mse}')
