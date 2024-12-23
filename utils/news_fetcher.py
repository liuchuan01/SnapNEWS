"""News fetching utility for SnapNews."""
from newsapi import NewsApiClient
from typing import List, Dict
import os
from dotenv import load_dotenv

class NewsFetcher:
    """Class to handle news fetching from NewsAPI."""
    
    def __init__(self):
        """Initialize the NewsFetcher with API key."""
        load_dotenv()
        self.api_key = os.getenv("NEWS_API_KEY")
        self.newsapi = NewsApiClient(api_key=self.api_key)
        
    def fetch_news(self, tags: List[str], limit: int = 40) -> List[Dict]:
        """Fetch news based on selected tags.
        
        Args:
            tags: List of selected tags
            limit: Number of news articles to fetch
            
        Returns:
            List of processed news articles
        """
        query = ' OR '.join(tags)
        
        try:
            news = self.newsapi.get_everything(
                q=query,
                language='zh',
                sort_by='publishedAt',
                page_size=limit
            )
            return self._process_news(news['articles'])
        except Exception as e:
            print(f"Error fetching news: {e}")
            return []
    
    def _process_news(self, articles: List[Dict]) -> List[Dict]:
        """Process raw news articles.
        
        Args:
            articles: Raw news articles from NewsAPI
            
        Returns:
            Processed news articles
        """
        processed = []
        for article in articles:
            processed.append({
                'title': article.get('title', ''),
                'description': article.get('description', ''),
                'url': article.get('url', ''),
                'source': article.get('source', {}).get('name', ''),
                'published_at': article.get('publishedAt', ''),
                'urlToImage': article.get('urlToImage', '')
            })
        return processed
