# News Aggregator

This is a Flask-based web application that aggregates news articles from various RSS feeds. It provides a simple interface to view the latest news from multiple sources and includes search and category filtering functionalities.

## Features

- Aggregates news from multiple sources including NYT, Washington Post, Huffington Post, The Guardian, Yahoo Finance, Hacker News, Wall Street Journal, and CNBC.
- Displays news articles sorted by publication date.
- Implements pagination for better user experience.
- Provides a search functionality to filter articles based on keywords.
- Allows filtering of articles by category (e.g., general, world, finance, technology).
- Implements caching to reduce the number of requests to RSS feeds.
- Includes error handling for improved reliability.

## Requirements

- Python 3.7+
- Flask
- feedparser

For a complete list of dependencies, see `requirements.txt`.

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/drivenone/news-aggregator.git
   cd news-aggregator
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

3. Browse the latest news articles, use the search functionality to find specific topics, or filter articles by category.

## Code Structure

- `app.py`: The main Flask application file.
  - `fetch_rss_feed(feed_url)`: Fetches and parses a single RSS feed. Results are cached to improve performance.
  - `fetch_all_feeds()`: Fetches all RSS feeds and compiles the articles list.
  - `index()`: Handles the main page route, displaying paginated articles with category filtering.
  - `search()`: Handles the search functionality with category filtering.

## Error Handling

The application includes error handling for RSS feed fetching. If a feed is unavailable or there's an error in parsing, the error is logged and the application continues to function with the available feeds.

## Caching

The application uses Python's `lru_cache` to cache the results of RSS feed fetching. This significantly reduces the number of requests to the RSS feeds, improving performance especially under heavy traffic.

## Category Filtering

Articles are categorized (e.g., general, world, finance, technology) based on their source. Users can filter articles by these categories both on the main page and in search results.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).