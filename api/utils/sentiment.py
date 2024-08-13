from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from transformers import pipeline

sentiment_analyzer = SentimentIntensityAnalyzer()
bert_sentiment_analyzer = pipeline('sentiment-analysis')

def get_sentiment_score(text):
    sentiment = sentiment_analyzer.polarity_scores(text)['compound']
    bert_sentiment = bert_sentiment_analyzer(text)[0]
    sentiment_score = (sentiment + (1 if bert_sentiment['label'] == 'POSITIVE' else -1)) / 2
    return sentiment_score
