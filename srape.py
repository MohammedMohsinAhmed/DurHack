import requests
from bs4 import BeautifulSoup
import os
import openai
import json


url = "https://finviz.com/news.ashx"
factors = ["Interest rates", "Economic indicators", "Political Events", "Trade Balance", "Geopolitical Tension"]


def create_url(country, factor):
	return f"https://news.google.com/search?q={country}%2Fus%20{factor}&hl=en-GB&gl=GB&ceid=GB%3Aen"


def get_url(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "html.parser")
	soup_list = soup.find_all("a")
	print(soup_list)
	# for i, item in enumerate(soup_list):
	# 	print(item)
	# 	break
	# 	item_text = item.find("h3")
	# 	print(item_text)
	# 	# print(item_text, baseurl + item['href'])
	# 	headlines[f"{i}:{item_text}"] = baseurl + item['href']
	# return(headlines)

url = create_url("UK", factors[0])
get_url(url)