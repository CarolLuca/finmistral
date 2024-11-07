# Financial Advisor Chatbot

This Financial Advisor Chatbot uses a machine learning model to provide stock analysis and financial advice based on user inputs. The chatbot leverages a language model to generate stock-related insights, utilizing sentiment analysis and historical data. Users can interact with the chatbot through a web interface built with Streamlit, allowing them to input questions and select stocks to analyze.

---

## Table of Contents
1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Setup](#setup)
4. [Configuration](#configuration)
5. [Usage](#usage)
6. [Code Overview](#code-overview)
7. [Limitations](#limitations)
8. [Contributing](#contributing)
9. [License](#license)

---

## Features

- **User Input for Financial Queries**: Users can enter questions related to stocks and receive data-driven responses.
- **Stock Selection**: Select specific stocks to analyze.
- **Real-time Stock Data**: The chatbot fetches and processes live data for stocks, including recent news and historical financial data.
- **Prompt Customization**: Generates tailored prompts for different types of responses, from simple summaries to more complex analyses.
- **Caching for Efficiency**: Implements caching for efficient data retrieval, minimizing redundant API calls.
- **Web Interface**: Built with Streamlit for an easy-to-use graphical interface.

---

## Prerequisites

Ensure you have the following installed:

- **Python 3.8+**
- **pip** (Python package manager)

Install the required packages by running:
```bash
pip install -r requirements.txt
```

With a simple command such as:
```bash
huggingface-cli download TheBloke/samantha-mistral-instruct-7B-GGUF samantha-mistral-instruct-7b.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```
you should be able to download a quantised version of Mistral Instruct.

---

## Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/CarolLuca/finmistral.git
   cd financial-advisor-chatbot
   ```

2. **Download and Configure the Llama Model**:
   - Place your Llama model file (e.g., `samantha-mistral-instruct-7b.Q4_K_M.gguf`) in the `models` directory.

3. **Configuration File (`config.py`)**:
   - Create a `config.py` file in the root directory with the following configurations:

     ```python
     # config.py

     # Number of news and financial entries per stock
     MAX_NEWS_ENTRIES = 5
     MAX_FINANCIAL_ENTRIES = 10

     # Stock options for the user interface
     STOCK_OPTIONS = ["AAPL", "GOOG", "AMZN", "MSFT", "TSLA"]  # Add stocks as needed

     # Caching configurations
     MAX_NEWS_CACHE_SIZE = 128
     ```

4. **Run the Application**:
   Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```
   This command will launch a local server, typically accessible at `http://localhost:8501`.

---

## Configuration

The chatbot's behavior is determined by configurations specified in `config.py`. Here are the main configuration options:

- **MAX_NEWS_ENTRIES**: Maximum number of recent news articles to retrieve for each stock.
- **MAX_FINANCIAL_ENTRIES**: Maximum number of financial data entries (e.g., daily prices) to retrieve.
- **STOCK_OPTIONS**: List of stock symbols available for selection in the UI.
- **MAX_NEWS_CACHE_SIZE**: Maximum cache size for news entries to limit memory usage.

Adjust these settings based on your application needs and available resources.

---

## Usage

1. **Launch the Chatbot**: Once the app is running, open the provided link in your browser (e.g., `http://localhost:8501`).

2. **Input Financial Query**: Enter a question related to financial advice or stock predictions in the input field.

3. **Select Stocks**: Choose one or more stocks to analyze from the provided list.

4. **Get Advice**: Click on the "Get Advice" button to receive the chatbot’s response based on current stock data and your input.

5. **Response**: The chatbot will analyze your question and selected stocks to generate a concise, data-driven response.

---

## Code Overview

### `url_scraper` (from `utils.py`)
Scrapes and returns the main text from the body of a specified URL. The text content, primarily paragraphs, is fetched and used in the financial context to analyze recent news articles related to the stock.

### `StockInfo` and `StocksManager` (from `data.py`)
- **StockInfo**: Stores information about a stock’s financial data and news articles.
- **StocksManager**: Handles the retrieval and caching of stock data, including fetching stock news and financial records using the `yfinance` library.

### `generate_prompt` (from `prompt.py`)
Creates a customized prompt based on the user’s question, selected stocks, and context. The prompt is tailored to either a simple or complex analysis based on the `complex` flag and includes placeholders for the stock information and the user’s question.

### Streamlit Application (`app.py`)
- **User Interface**: Created using Streamlit components, such as `st.text_input` for entering a question, `st.multiselect` for choosing stocks, and `st.button` for submitting.
- **Response Generation**: The `Llama` model receives the prompt created by `generate_prompt` and generates a response. This response is displayed as advice or prediction based on recent data for the selected stocks.

---