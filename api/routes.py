from flask import Blueprint, request, jsonify
from .utils.scoring import score_heading, score_subheading

main = Blueprint('main', __name__)

@main.route('/process', methods=['POST'])
def process_data():
    data = request.json
    print(f"Received data: {data}")  # Add logging to see received data
    data_type = data.get('dataType')
    data_body = data.get('dataBody')

    # Perform content scoring based on dataType
    if data_type and data_body:
        if data_type == 'heading':
            score = score_heading(data_body)
        elif data_type == 'subheading':
            score = score_subheading(data_body)
        else:
            return jsonify({'error': 'Invalid dataType'}), 400

        return jsonify({'score': score}), 200
    else:
        return jsonify({'error': 'Invalid input'}), 400
