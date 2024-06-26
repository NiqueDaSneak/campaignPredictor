import pandas as pd
from joblib import load

def load_model(model_path):
    model = load(model_path)
    return model

def make_predictions(model, X):
    predictions = model.predict(X)
    return predictions
