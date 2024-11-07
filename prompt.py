# Importing StocksManager and StockInfo classes for managing and retrieving stock data
from data import StocksManager, StockInfo

# Importing prompt format templates and tokens from the utils module
from utils import (
    PROMPT_FORMAT,
    QUERY_TOKEN,
    DESCRIPTION_TOKEN,
    SIMPLE_CONTEXT_PROMPT,
    COMPLEX_CONTEXT_PROMPT,
)

# Importing configuration settings
import config

# Importing regular expressions module for text substitution
import re


def generate_prompt(
    stocks_manager: StocksManager,
    input_text: str,
    input_stocks: list[str],
    complex: bool,
) -> dict:
    """
    Generates a structured prompt with stock information to assist in financial analysis.

    Args:
        stocks_manager (StocksManager): An instance of StocksManager to retrieve stock data.
        input_text (str): The client's question or input to include in the prompt.
        input_stocks (list[str]): A list of stock symbols to retrieve information for.
        complex (bool): Determines whether to use the complex or simple prompt format.

    Returns:
        dict: A structured message dictionary to be used in the prompt, containing the
              system message (context) and user message (generated prompt).
    """
    # Calculate the number of news and financial entries per stock based on total stocks
    stock_count = len(input_stocks)
    news_entr_ps = max(1, config.MAX_NEWS_ENTRIES // stock_count)
    fin_entr_ps = max(3, config.MAX_FINANCIAL_ENTRIES // stock_count)

    # Collect descriptive data for each stock based on the available entries
    helpful_data = ""
    for stock in input_stocks:
        # Retrieve stock info for each stock symbol
        stock_info: StockInfo = stocks_manager.get_info(stock)
        # Generate a description containing news and financial data for each stock
        description = stock_info.get_description(news_entr_ps, fin_entr_ps)
        # Append stock symbol and description to helpful_data
        helpful_data += f"{stock}\n{description}\n"

    # Format the prompt by inserting client question and stock data
    prompt = PROMPT_FORMAT
    prompt = re.sub(QUERY_TOKEN, input_text, prompt)
    prompt = re.sub(DESCRIPTION_TOKEN, helpful_data, prompt)

    # Construct the message structure with context and user prompt
    messages = [
        {
            "role": "system",
            "content": (
                # Use complex or simple context prompt based on the 'complex' flag
                COMPLEX_CONTEXT_PROMPT
                if complex
                else SIMPLE_CONTEXT_PROMPT
            ),
        },
        {"role": "user", "content": prompt},
    ]

    return messages
