import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article
import openai
import os
import tiktoken
import time
from url_to_summary import send


def get_positivity(summary, country):
    with open("secrets.txt", "r") as file:
        openai.api_key = api_key = json.load(file)['openai_key']
    prompt = f'''
	you are only to respond with a number (-1,1) based on how Positive you as an expert believe the summary for increase the price of {country}'s currency, you will not respond with anything other than an 3dp number in this interval, no polite explanation,
	'''
    response = send(prompt=prompt, text_data=summary)
    return (response[0])


if __name__ == '__main__':
    example_summary = '''
	According to a note from Deutsche Bank, the Japanese yen's fundamentals are weak, making it comparable to currencies like the Turkish lira and Argentine peso. The note suggests that factors like yields and external accounts contribute to the yen's poor performance.
	'''
    print(get_importance(example_summary, 'UK'))
