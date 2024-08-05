from flask import Flask, request, jsonify
from flask_cors import CORS
import textstat
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

sentiment_analyzer = SentimentIntensityAnalyzer()
bert_sentiment_analyzer = pipeline('sentiment-analysis')

@app.route('/process', methods=['POST'])
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

def score_heading(text):
    readability_score = textstat.flesch_reading_ease(text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    length_score = 1 if 50 <= len(text) <= 60 else 0
    keyword_density_score = calculate_keyword_density(text, 1, 2)
    sentiment_score = get_sentiment_score(text)
    
    final_score = (readability_score / 100) + length_score + keyword_density_score + sentiment_score
    return {
        'quality': 'high' if final_score > 2.5 else 'medium' if final_score > 1.5 else 'low',
        'recommendations': generate_recommendations(readability_score, length_score, keyword_density_score, sentiment_score)
    }

def score_subheading(text):
    readability_score = textstat.flesch_reading_ease(text)
    flesch_kincaid_grade = textstat.flesch_kincaid_grade(text)
    length_score = 1 if 150 <= len(text) <= 160 else 0
    keyword_density_score = calculate_keyword_density(text, 1, 2)
    sentiment_score = get_sentiment_score(text)
    
    final_score = (readability_score / 100) + length_score + keyword_density_score + sentiment_score
    return {
        'quality': 'high' if final_score > 2.5 else 'medium' if final_score > 1.5 else 'low',
        'recommendations': generate_recommendations(readability_score, length_score, keyword_density_score, sentiment_score)
    }

def calculate_keyword_density(text, min_count, max_count):
    # This is a placeholder function. You need to implement your keyword extraction and density calculation.
    # For example, use nltk or spaCy to extract keywords and calculate their frequency.
    # Here, we assume keyword density is optimal and return 1.
    return 1

def get_sentiment_score(text):
    sentiment = sentiment_analyzer.polarity_scores(text)['compound']
    bert_sentiment = bert_sentiment_analyzer(text)[0]
    sentiment_score = (sentiment + (1 if bert_sentiment['label'] == 'POSITIVE' else -1)) / 2
    return sentiment_score

def generate_recommendations(readability_score, length_score, keyword_density_score, sentiment_score):
    recommendations = []
    if readability_score < 60:
        recommendations.append('Improve readability')
    if length_score == 0:
        recommendations.append('Adjust length to optimal range')
    if keyword_density_score == 0:
        recommendations.append('Optimize keyword density')
    if sentiment_score < 0:
        recommendations.append('Improve sentiment')
    return recommendations

if __name__ == '__main__':
    app.run(debug=True)
