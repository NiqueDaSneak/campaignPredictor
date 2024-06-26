import pandas as pd
import joblib
import sys

def load_model(model_path):
    """Load the trained model from a file."""
    return joblib.load(model_path)

def make_predictions(model, input_data):
    """Make predictions using the trained model."""
    predictions = model.predict(input_data)
    return predictions

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python predict.py <input_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]

    # Load the input data
    input_data = pd.read_csv(input_csv)

    # Load the trained model
    model = load_model('models/training/model.joblib')

    # Make predictions
    predictions = make_predictions(model, input_data)

    # Print the predictions
    print("Predictions:")
    print(predictions)

    # Optionally, save the predictions to a CSV file
    output_csv = input_csv.replace('.csv', '_predictions.csv')
    pd.DataFrame(predictions, columns=['Prediction']).to_csv(output_csv, index=False)
    print(f"Predictions saved to {output_csv}")
