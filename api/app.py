from flask import Flask, request, jsonify
from predict import predict

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    data = request.get_json()
    campaign_details = {
        'goal_amount': data['goal_amount'],
        'backers': data['backers']
    }
    prediction = predict(campaign_details)
    return jsonify({'predicted_amount_raised': prediction})

if __name__ == '__main__':
    app.run(debug=True)
