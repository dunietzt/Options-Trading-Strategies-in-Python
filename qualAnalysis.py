import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import logging
import json
from functools import lru_cache

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=128)
def get_sentiment_score(article):
    """
    Function to get sentiment score of a news article using NLTK Vader sentiment analysis.
    """
    try:
        sid = SentimentIntensityAnalyzer()
        sentiment_score = sid.polarity_scores(article)['compound']
        return sentiment_score
    except Exception as e:
        logger.error("Error getting sentiment score: %s", str(e))
        return 0

@lru_cache(maxsize=128)
def get_news_articles(symbol, news_sources, news_api_key):
    """
    Function to get news articles related to a given symbol from News API.
    """
    try:
        url = f'https://newsapi.org/v2/everything?q={symbol}&sources={news_sources}&apiKey={news_api_key}'
        response = requests.get(url)
        data = response.json()
        if 'articles' in data:
            articles = [article['description'] for article in data['articles']]
            return articles
        else:
            return []
    except Exception as e:
        logger.error("Error getting news articles: %s", str(e))
        return []

@lru_cache(maxsize=128)
def get_analyst_recommendations(symbol, api_key):
    """
    Function to get analyst recommendations for a given symbol from Alpha Vantage.
    """
    try:
        url = f'https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={api_key}'
        response = requests.get(url)
        data = response.json()
        if 'AnalystRating' in data:
            return int(data['AnalystRating'])  # Convert to int
        else:
            return 0
    except Exception as e:
        logger.error("Error getting analyst recommendations: %s", str(e))
        return 0

def get_financial_sentiment(symbol, news_sources, news_api_key, api_key):
    """
    Function to compute the overall strength value based on sentiment analysis of news articles and analyst recommendations.
    """
    try:
        articles = get_news_articles(symbol, news_sources, news_api_key)
        if not articles:
            logger.warning("No news articles found for symbol %s", symbol)
            return 0

        total_sentiment_score = sum(get_sentiment_score(article) for article in articles) / len(articles)
        analyst_recommendations = get_analyst_recommendations(symbol, api_key)
        overall_strength = total_sentiment_score + analyst_recommendations
        return overall_strength
    except Exception as e:
        logger.error("Error computing overall strength: %s", str(e))
        return 0

if __name__ == "__main__":
    try:
        # Configuration
        company = 'AAPL'  # Specify the company symbol
        news_sources = 'bbc-news, bloomberg, cnn, reuters'  # Specify news sources
        news_api_key = 'YOUR_NEWS_API_KEY'
        api_key = 'YOUR_ALPHA_VANTAGE_API_KEY'

        # Get overall strength
        strength = get_financial_sentiment(company, news_sources, news_api_key, api_key)
        print("Overall Strength:", strength)
    except Exception as e:
        logger.error("Error in main: %s", str(e))