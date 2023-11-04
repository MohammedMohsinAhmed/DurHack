import requests
from bs4 import BeautifulSoup

url = "https://www.bbc.co.uk/news"
baseurl = "https://www.bbc.co.uk"
response = requests.get(url)

if response.status_code == 200:
    """
    soup = BeautifulSoup(response.text, "html.parser")
    soup_list = soup.find_all("h3")
    for item in soup_list:
        item_text = item.get_text()
        print(item_text)
    """
    soup = BeautifulSoup(response.text, "html.parser")
    soup_list = soup.find_all("a", href=True, class_="gs-c-promo-heading gs-o-faux-block-link__overlay-link gel-pica-bold nw-o-link-split__anchor")
    for item in soup_list:
        item_text = item.find("h3").get_text()
        print(item_text, baseurl + item['href'])

        # concat link with https://www.bbc.co.uk/