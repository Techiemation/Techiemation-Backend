import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    # Send a GET request to the URL
    response = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the page has an <article> tag
    result = ""
    article = soup.find("article")
    if article:
        # Get all the data inside the <article> tag
        result = article.get_text()
        # print("Article Data:")
        # return article_data

    elif soup.find("main"):
        # If there's no <article> tag, check for a <main> tag
        result = soup.find("main").get_text()
        # print("Main Content:")
        # return main_content
    else:
        # If neither <article> nor <main> tag is found, get the content of the <body> tag
        result = soup.find("body").get_text()
        # print("Body Content:")
        # return body_content
    return result

# if __name__ == "__main":
    # url = "https://developer.mozilla.org/en-US/docs/Web/HTML"
    # website_data = scrape_website(url)
    # print(website_data)