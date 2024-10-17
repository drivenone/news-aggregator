import feedparser
from flask import Flask, render_template, request
from functools import lru_cache
import time
from collections import defaultdict

app = Flask(__name__)

# Dictionary of RSS feed URLs, their corresponding source names, and categories
RSS_FEEDS = {
    'https://www.nytimes.com/services/xml/rss/nyt/HomePage.xml': ('NYT', 'general'),
    'https://www.washingtonpost.com/rss/national': ('Washington Post', 'general'),
    'https://www.huffingtonpost.com/feed/': ('Huffington Post', 'general'),
    'https://www.theguardian.com/world/rss': ('The Guardian', 'world'),
    'https://finance.yahoo.com/news/rssindex': ('Yahoo Finance', 'finance'),
    'https://news.ycombinator.com/rss': ('Hacker News', 'technology'),
    'https://feed.a.dj.com/rss/RSSMarketsMain.xml': ('Wall Street Journal', 'finance'),
    'https://search.cnbc.com/rs/search/combinecms/view.xml?partnerId=wrss01&id15839069': ('CNBC', 'finance')
}

@lru_cache(maxsize=len(RSS_FEEDS))
def fetch_rss_feed(feed_url):
    try:
        return feedparser.parse(feed_url)
    except Exception as e:
        print(f"Error fetching RSS feed {feed_url}: {str(e)}")
        return None

def fetch_all_feeds():
    articles = []
    for feed_url, (source, category) in RSS_FEEDS.items():
        parsed_feed = fetch_rss_feed(feed_url)
        if parsed_feed and parsed_feed.entries:
            entries = [(source, category, entry) for entry in parsed_feed.entries]
            articles.extend(entries)
    return articles

@app.route('/')
def index():
    articles = fetch_all_feeds()
    category = request.args.get('category', 'all')
    
    # Filter articles by category if a specific category is selected
    if category != 'all':
        articles = [article for article in articles if article[1] == category]
    
    # Sort articles by publication date (newest first)
    articles = sorted(articles, key=lambda x: x[2].get('published_parsed', time.gmtime(0)), reverse=True)
    
    # Implement pagination
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    total_articles = len(articles)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]
    
    # Get all unique categories
    categories = sorted(set(category for _, category, _ in articles))
    
    return render_template('index.html', articles=paginated_articles, page=page,
                           total_articles=total_articles // per_page + 1,
                           categories=categories, selected_category=category)

@app.route('/search')
def search():
    query = request.args.get('query', '').lower()
    category = request.args.get('category', 'all')
    articles = fetch_all_feeds()
    
    # Filter articles based on search query and category
    results = [article for article in articles 
               if query in article[2].title.lower() 
               and (category == 'all' or article[1] == category)]
    
    # Get all unique categories
    categories = sorted(set(category for _, category, _ in articles))
    
    return render_template('search.html', articles=results, query=query,
                           categories=categories, selected_category=category)

if __name__ == '__main__':
    app.run(debug=True)