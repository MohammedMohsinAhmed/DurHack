import requests
import json
from bs4 import BeautifulSoup
from newspaper import Article
import openai
import os
import tiktoken
import time
from url_to_summary import send
import re
import statistics


def get_response(prompt, text_data):
    openai.api_base = "http://llama.qrt.services:8000/v1"
    openai.api_key = ""
    completion = openai.ChatCompletion.create(
        model="local-model",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_data}
        ],
        n_ctx=4096,
        max_tokens=1000,
        temperature=2
    )
    return (completion.choices[0].message)


def get_importance(summary, country):
    with open("secrets.txt", "r") as file:
        openai.api_key = api_key = json.load(file)['openai_key']
    prompt = f'''
	TAKE YOUR TIME, you are only to respond with a number (00 to 10) based on how important the summary is for increase the price of {country}'s currency, you will not respond with anything other than an integer in this interval, do not give a polite explanation
	'''
    response = get_response(
        prompt=prompt, text_data=summary)
    try:
        result = int(response.content)
    except:
        print(response)
        try:
            result = re.findall(r'\b\d{2}\b', response.content)[-1]
        except:
            result = 5

    return (int(result))
    # print(response)
    # return (int(response))


if __name__ == '__main__':
    example_summary = '''
	According to a note from Deutsche Bank, the Japanese yen's fundamentals are weak, making it comparable to currencies like the Turkish lira and Argentine peso. The note suggests that factors like yields and external accounts contribute to the yen's poor performance.
	'''
    print(get_importance(example_summary, 'UK'))
