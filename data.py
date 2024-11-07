# Importing ExpiringDict for caching stock data with expiration and limiting capacity
from expiringdict import ExpiringDict

# Importing NamedTuple for structured data storage in a named format
from typing import NamedTuple

# Importing yfinance library to retrieve stock data
import yfinance as yf

# Importing pandas for data manipulation
import pandas as pd

# Importing functools for function caching capabilities
import functools

# Importing a custom URL scraper function from utils module
from utils import url_scraper


# Define a NamedTuple to store stock-related information
class StockInfo(NamedTuple):
    # List of news entries related to the stock
    news: list[str]
    # DataFrame containing financial data (e.g., stock history)
    financials: pd.DataFrame

    def get_description(self, news_entries: int, financial_entries: int) -> str:
        """
        Generates a text description containing specified numbers of financial
        and news entries.

        Args:
            news_entries (int): Number of news items to include in the description.
            financial_entries (int): Number of financial rows to include in the description.

        Returns:
            str: A formatted string containing financial data and news.
        """
        # Add the requested number of financial entries to the description
        description = f"Financials:\n{self.financials[:financial_entries]}\n"
        description += "News:\n"
        # Add the requested number of news entries to the description
        for index, entry in enumerate(self.news[:news_entries]):
            description += f"[{index}] - {entry}\n"
        return description


# Class to manage stock data retrieval and caching
class StocksManager:
    def __init__(self):
        # Initialize an ExpiringDict to cache stock data, with a max size and expiration time
        self.stocks = ExpiringDict(max_len=128, max_age_seconds=300)

    @functools.cache
    def __get_ticker__(stock: str) -> yf.Ticker:
        """
        Retrieves a ticker object for a given stock symbol.

        Args:
            stock (str): The stock symbol (ticker).

        Returns:
            yf.Ticker: A yfinance Ticker object for the specified stock.
        """
        return yf.Ticker(stock)

    def __get_news__(ticker: yf.Ticker) -> list[str]:
        """
        Retrieves the latest news for a given ticker.

        Args:
            ticker (yf.Ticker): The yfinance Ticker object for the stock.

        Returns:
            list[str]: A list of formatted news articles, including titles and main content.
        """
        # Retrieve the first five news references from the ticker
        references = ticker.news[:5]
        news = []

        # Extract and format the title and main content of each news article
        for instance in references:
            title = instance["title"]
            main_text = url_scraper(instance["link"])
            news.append(f'{title}\n"{main_text}"')

        return news

    def __get_financials__(ticker: yf.Ticker) -> pd.DataFrame:
        """
        Retrieves the historical financial data for a given ticker.

        Args:
            ticker (yf.Ticker): The yfinance Ticker object for the stock.

        Returns:
            pd.DataFrame: A DataFrame containing historical financial data for the past month.
        """
        # Retrieve the last month's historical data for the ticker
        return ticker.history("1mo")

    def get_info(self, stock: str) -> StockInfo:
        """
        Gets stock information (news and financials) for a given stock symbol.
        If data is cached, it retrieves from cache; otherwise, it fetches new data.

        Args:
            stock (str): The stock symbol (ticker).

        Returns:
            StockInfo: A StockInfo object containing news and financial data.
        """
        # Check if stock information is already cached
        stock_info = self.stocks.get(stock, None)
        if stock_info is None:
            # Fetch new data if not cached
            ticker = StocksManager.__get_ticker__(stock)
            stock_info = StockInfo(
                news=StocksManager.__get_news__(ticker),
                financials=StocksManager.__get_financials__(ticker),
            )
            # Cache the fetched data
            self.stocks[stock] = stock_info

        return stock_info
