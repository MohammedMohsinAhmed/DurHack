import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article
import openai
import os
import tiktoken
import time


def send(
    prompt=None,
    text_data=None,
    chat_model="local-model",
    model_token_limit=8192,
    max_tokens=250,
    n_ctx=4096,
    temperature=0
):
    """
    Send the prompt at the start of the conversation and then send chunks of text_data to ChatGPT via the OpenAI API.
    If the text_data is too long, it splits it into chunks and sends each chunk separately.

    Args:
    - prompt (str, optional): The prompt to guide the model's response.
    - text_data (str, optional): Additional text data to be included.
    - max_tokens (int, optional): Maximum tokens for each API call. Default is 2500.

    Returns:
    - list or str: A list of model's responses for each chunk or an error message.
    """
    # Set up your OpenAI API key
    # Load your API key from an environment variable or secret management service
    # Read and load the variables from "secrets.txt"

    openai.api_base = "http://llama.qrt.services:8000/v1"
    openai.api_key = ""
    # Check if the necessary arguments are provided
    if not prompt:
        return "Error: Prompt is missing. Please provide a prompt."
    if not text_data:
        return "Error: Text data is missing. Please provide some text data."

    # tokenizer = tiktoken.encoding_for_model(chat_model)

    tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

    token_integers = tokenizer.encode(text_data)

    # Split the token integers into chunks based on max_tokens
    chunk_size = max_tokens - len(tokenizer.encode(prompt))
    chunks = [
        token_integers[i: i + chunk_size]
        for i in range(0, len(token_integers), chunk_size)
    ]

    # Decode token chunks back to strings
    chunks = [tokenizer.decode(chunk) for chunk in chunks]

    responses = []
    messages = [
        {"role": "user", "content": prompt},
        {
            "role": "user",
            "content": "To provide the context for the above prompt, I will send you text in parts. When I am finished, I will tell you 'ALL PARTS SENT'. Do not answer until you have received all the parts.",
        },

    ]
    chunk = chunks[0]
    messages.append({"role": "user", "content": chunk})
    while (
        sum(len(tokenizer.encode(msg["content"])) for msg in messages)
        > model_token_limit
    ):
        messages.pop(1)  # Remove the oldest chunk
        response = openai.ChatCompletion.create(
            model=chat_model, messages=messages, n_ctx=n_ctx, max_tokens=max_tokens, temperature=0)
        chatgpt_response = response.choices[0].message["content"].strip()
        responses.append(chatgpt_response)

    # Add the final "ALL PARTS SENT" message
    messages.append({"role": "user", "content": "ALL PARTS SENT"})
    response = openai.ChatCompletion.create(
        model=chat_model, messages=messages, n_ctx=n_ctx, max_tokens=max_tokens, temperature=temperature)
    final_response = response.choices[0].message["content"].strip()
    responses.append(final_response)

    return responses


def get_summary(url):
    # with open("secrets.txt", "r") as file:
    # 	openai.api_key = api_key = json.load(file)['openai_key']
    url_response = requests.get(url)
    soup = BeautifulSoup(url_response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    prompt_text = "Summarize the following text for me in 50 words:"
    print(1)
    start = time.time()
    responses = send(prompt=prompt_text, text_data=str(paragraphs))
    end = time.time()
    print(end-start)
    summary = responses[0]
    return summary


if __name__ == '__main__':
    print(get_summary("https://www.bbc.co.uk/news/business-67290817"))
