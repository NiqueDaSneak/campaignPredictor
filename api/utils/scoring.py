import textstat
from .sentiment import get_sentiment_score
from .text_processing import calculate_keyword_density, generate_recommendations

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
