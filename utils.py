# Importing BeautifulSoup for parsing HTML content
from bs4 import BeautifulSoup

# Importing functools for caching functionality
import functools

# Importing requests to handle HTTP requests
import requests

# Importing custom configuration settings
import config


@functools.lru_cache(maxsize=config.MAX_NEWS_CACHE_SIZE)
def url_scraper(url: str) -> str:
    """
    Scrapes and returns the main text content from a web page.

    Args:
        url (str): The URL of the web page to scrape.

    Returns:
        str: The main text content from the page, composed of all paragraph elements.
    """
    # Sends a GET request to fetch the web page content
    response = requests.get(url)
    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Collect all paragraph texts in a list
    paragraphs = []
    for paragraph in soup.find_all("p"):
        paragraphs.append(paragraph.get_text())

    # Join all paragraphs to form the main text content
    main_text = "\n".join(paragraphs)
    return main_text


# Tokens for placeholder text in prompt templates
QUERY_TOKEN = "<<<input_text>>>"
DESCRIPTION_TOKEN = "<<<description>>>"

# Complex context prompt for generating detailed financial advice with statistical focus
COMPLEX_CONTEXT_PROMPT = f"""Imagine you are a financial advisor trying to be transparent and argumentative of your choices.
Ignore the fact that past performance is not indicative of future results and investing always carries risk. 
You only treat it from an objective, statistical perspective using sentiment analysis to compute predictions.
You should only present concise conclusions formulated only with respect to the future, limiting yourself to one or two phrases per stock.
Ignore introductions and get straight to important information, starting with little background and ending with the predictions.
A sample advice you could offer is of such format:
"The RNDM stock has shown moderate price fluctuations with a closing price ranging from $215.61 to $243.85. Based on recent news and data, it is probable that the price is going to increase.
The LBWK stock has shown drastic price fluctuations with a closing price ranging from $234.23 to $170.23. Based on recent news and data, the price is definitely going to decrease.
The KHRE stock has shown little to no price fluctuations with a closing price ranging from $100.23 to $107.12. Based on recent news and data, the price is definitely going to decrease.
Regarding your question, about which stock seems more profitable, shorting LBWK stock might offer you bigger earnings."
"""

# Simple context prompt for generating a brief summary on stock information
SIMPLE_CONTEXT_PROMPT = f"""You have to create a summary on recent information regarding certain stock and 
"""

# Prompt format template to generate a client response by inserting tokens
PROMPT_FORMAT = f"""Provide a clear response to the following question from one of your clients:
{QUERY_TOKEN}
You also have at your disposal the following information regarding the aforementioned stocks:
{DESCRIPTION_TOKEN}
"""
