import streamlit as st
import requests
import json
from url_to_summary import get_summary
from get_importance import get_importance
from get_positivity import get_positivity

# Define a mapping from country to currency
country_to_currency = {
    "usa": "USD",
    "eurozone": "EUR",
    "japan": "JPY",
    "uk": "GBP",
    "australia": "AUD",
    # Add more countries and their respective currencies here
}
left_overall = 0
right_overall = 0

# Define a function to fetch articles
st.set_page_config(layout="wide")


@st.cache_data
def fetch_articles(api_key, country, factors):
    search_query = " OR ".join(factors)
    search_query_encoded = requests.utils.quote(search_query)
    url = f'https://newsapi.org/v2/everything?q={country} AND ({search_query_encoded})&apiKey={api_key}'
    response = requests.get(url)

    if response.status_code == 200:
        return response.json().get('articles')
    else:
        st.error(f"Failed to fetch articles: HTTP {response.status_code}")
        return []


# Load the API key once and store it in an environment variable or session state
if 'api_key' not in st.session_state:
    with open("secrets.txt", "r") as file:
        st.session_state['api_key'] = json.load(file)['api_key']

st.markdown("<h1 style='text-align: center;'>FX News App</h1>",
            unsafe_allow_html=True)

# Create two columns for the separate filters and results
col1, col2 = st.columns(2)

# Initialize session state for articles in both columns
if 'articles_left' not in st.session_state:
    st.session_state['articles_left'] = []
if 'articles_right' not in st.session_state:
    st.session_state['articles_right'] = []

# Column 1
with col1:
    # Left search
    country_left = st.text_input('Enter Country', key='country_left').lower()
    currency_left = country_to_currency.get(
        country_left, "Currency not found")
    # Display the currency for confirmation
    st.text(f"Currency: {currency_left}")
    factors_left = st.multiselect(
        'Choose Categories',
        ["Interest rates", "Economic indicators", "Political Events",
            "Trade Balance", "Geopolitical Tension"],
        default=["Interest rates"],
        key='factors_left'
    )
    ll_col, lr_col = st.columns(2)
    btn_left = ll_col.button('Search Left', key='btn_left')

    if btn_left:
        st.session_state['articles_left'] = fetch_articles(
            st.session_state['api_key'], country_left, factors_left)

    for count, article in enumerate(st.session_state['articles_left']):
        if count == 5:
            break
        with st.expander(article['title']):
            st.write(article.get('description', get_summary(article['url'])))
            importance_rating = get_importance(article.get(
                'description', get_summary(article['url'])), country_left)
            positivity_rating = get_positivity(article.get(
                'description', get_summary(article['url'])), country_left)
            left_overall += int(importance_rating)*float(positivity_rating)
            st.write(f"Importance Rating: {importance_rating}")
            st.write(f"Positivity Rating: {positivity_rating}")

        st.markdown(
            f"[Read full article]({article['url']})", unsafe_allow_html=True)
    lr_col.write(f"Overall Score: {round(left_overall/5, 2)}")

# Column 2
with col2:
    # Right search
    country_right = st.text_input('Enter Country', key='country_right').lower()
    currency_right = country_to_currency.get(
        country_right, "Currency not found")
    # Display the currency for confirmation
    st.text(f"Currency: {currency_right}")
    factors_right = st.multiselect(
        'Choose Categories',
        ["Interest rates", "Economic indicators", "Political Events",
            "Trade Balance", "Geopolitical Tension"],
        default=["Interest rates"],
        key='factors_right'
    )
    rl_col, rr_col = st.columns(2)
    btn_right = rl_col.button('Search Right', key='btn_right')

    if btn_right:
        st.session_state['articles_right'] = fetch_articles(
            st.session_state['api_key'], country_right, factors_right)

    for count, article in enumerate(st.session_state['articles_right']):
        if count == 5:
            break
        with st.expander(article['title']):
            st.write(article.get('description', get_summary(article['url'])))
            importance_rating = get_importance(article.get(
                'description', get_summary(article['url'])), country_right)
            positivity_rating = get_positivity(article.get(
                'description', get_summary(article['url'])), country_right)
            right_overall += int(importance_rating)*float(positivity_rating)
            st.write(f"Importance Rating: {importance_rating}")
            st.write(f"Positivity Rating: {positivity_rating}")

        st.markdown(
            f"[Read full article]({article['url']})", unsafe_allow_html=True)
    rr_col.write(f"Overall Score: {round(right_overall/5, 2)}")
