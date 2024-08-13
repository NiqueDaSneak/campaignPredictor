def calculate_keyword_density(text, min_count, max_count):
    # This is a placeholder function. You need to implement your keyword extraction and density calculation.
    # For example, use nltk or spaCy to extract keywords and calculate their frequency.
    # Here, we assume keyword density is optimal and return 1.
    return 1

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
