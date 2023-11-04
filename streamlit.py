import streamlit as st
import requests
import json

# Read and load the variables from "secrets.txt"
with open("secrets.txt", "r") as file:
    api_key = json.load(file)['api_key']

st.title('FX News App')

# Use sidebar for input and article selection
with st.sidebar:
    country = st.text_input('Enter Country')

    factors = st.multiselect(
        'Choose Categories', 
        ["Interest rates", "Economic indicators", "Political Events", "Trade Balance", "Geopolitical Tension"],
        default=["Interest rates"]
    )

    btn = st.button('Search')

# Main area for AI summary and article content
article_container = st.container()
summary_container = st.container()

if btn:
    search_query = " OR ".join(factors)
    search_query_encoded = requests.utils.quote(search_query)
    url = f'https://newsapi.org/v2/everything?q={country} AND ({search_query_encoded})&apiKey={api_key}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        articles = data.get('articles')

        if articles:
            # Create a select box for article titles
            article_titles = [article.get('title') for article in articles]
            selected_title = st.sidebar.selectbox('Select an article', article_titles)
            selected_article = next((article for article in articles if article.get('title') == selected_title), None)

            if selected_article:
                # Display the AI summary
                with summary_container:
                    st.subheader('AI Summary')
                    # Placeholder for AI-generated summary
                    st.write('AI-generated summary will go here...')

                # Display the article content
                with article_container:
                    st.subheader(selected_title)
                    st.markdown(f"[Read full article]({selected_article.get('url')})", unsafe_allow_html=True)
                    # You can add an iframe or another method to display the article content here
                    # st.write('Article content will go here...')
        else:
            st.sidebar.error("No articles found for the selected criteria.")
    else:
        st.sidebar.error("Failed to fetch articles.")
        
# Function to display articles in the sidebar with a scrollbar if needed
def display_articles(articles):
    with st.sidebar:
        st.subheader("Articles")
        for article in articles:
            if st.button(article['title'], key=article['title']):
                # Display the AI summary
                with summary_container:
                    st.subheader('AI Summary')
                    # Placeholder for AI-generated summary
                    st.write('AI-generated summary will go here...')
                
                # Display the article content
                with article_container:
                    st.subheader(article['title'])
                    st.markdown(f"[Read full article]({article['url']})", unsafe_allow_html=True)
                    # You can add an iframe or another method to display the article content here
                    # st.write('Article content will go here...')


