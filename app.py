# Importing Llama model class for generating AI-based responses
from llama_cpp import Llama
# Importing Streamlit for building a web-based user interface
import streamlit as st

# Importing StocksManager for managing and retrieving stock data
from data import StocksManager
# Importing function to generate prompts
from prompt import generate_prompt
# Importing configuration settings
import config

# Initialize the StocksManager instance to handle stock data
stocks_manager = StocksManager()

# Initialize the Llama language model with specified model path and context length
llm = Llama(
    model_path="./models/samantha-mistral-instruct-7b.Q4_K_M.gguf",
    n_ctx=9000,  # Context length for managing longer conversations or inputs
)

# Streamlit app title
st.title("Financial Advisor Chatbot")

# User input field for entering a financial question
user_input = st.text_input("Enter your financial question:")
# Multiselect input for choosing which stocks to analyze
selected_stocks = st.multiselect("Select stocks to analyze:", config.STOCK_OPTIONS)

# Button to submit the question and selected stocks for analysis
if st.button("Get Advice"):
    # Check if both user input and stock selection are provided
    if user_input and selected_stocks:
        # Generate a prompt based on user input, selected stocks, and default context
        prompt = generate_prompt(stocks_manager, user_input, selected_stocks, False)
        # Concatenate prompt content to prepare for model input
        input_text = "".join([entry["content"] for entry in prompt])
        
        # Generate response using Llama model, limiting token output and defining stop criteria
        response = llm(
            input_text,
            max_tokens=32,  # Limits response length
            stop=["\n", "?"],  # Stop conditions for response truncation
        )
        # Display the response in the Streamlit app
        st.write(response)
    else:
        # Display error if required inputs are missing
        st.error("Please enter a financial question and select at least one stock.")
