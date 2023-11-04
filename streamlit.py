import streamlit as st
import requests
import pycountry
import json

# Read and load the variables from "secrets.txt"
with open("secrets.txt", "r") as file:
    api_key = json.load(file)['api_key']
    
search = 'UK and US Interest rates, Economic indicators, Political Events'
# Construct the API URL
url = f'https://newsapi.org/v2/everything?q={search}&apiKey={api_key}'
response = requests.get(url)


st.title('FX News App')


col1, col2 = st.columns(2)
with col1:
	country = st.text_input('Enter Country')

with col2:
	factor = st.radio('Choose Cateogry', ("Interest rates", "Economic indicators", "Political Events", "Trade Balance", "Geopolitical Tension"))
	btn = st.button('Enter')

if btn:
	url = f'https://newsapi.org/v2/everything?q={country}&apiKey={api_key}'
	response = requests.get(url)
	if response.status_code == 200:
		
		data = response.json()
		articles = data.get('articles')

		if articles:
			for article in articles:     
				title = article.get('title')
				url = article.get('url')
				published_at = article.get('publishedAt')
				# image = article.get('urlToImage')
				st.write(title)
				st.write(url)
				st.write(published_at)