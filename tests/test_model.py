import unittest
import joblib
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from data_preprocessing.preprocess import preprocess_data
from data_preprocessing.train_test_split import split_data

class TestModel(unittest.TestCase):
    def setUp(self):
        self.model = joblib.load('../models/model.joblib')

    def test_model_performance(self):
        df = pd.read_sql('SELECT * FROM campaigns', engine)
        X_train, X_test, y_train, y_test = split_data(df)
        X_test = preprocess_data(X_test)
        y_pred = self.model.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        self.assertLess(mse, 100000)  # Example threshold

if __name__ == '__main__':
    unittest.main()
