import requests
from bs4 import BeautifulSoup

query = input("Enter your query: ")
print("Searching for:", query)

# URL for the website search
url = f"https://help.appdirect.com/hc/en-us/search?utf8=%E2%9C%93&query={query}&commit=Search"

# Setting user-agent header to avoid detection as a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Sending request to the website search and retrieving HTML content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extracting search results
search_results = soup.select("div.results-container > ul > li")

if len(search_results) > 0:
    # Extracting and printing the first search result
    first_result = search_results[0]
    title = first_result.select_one("h3 > a").get_text()
    link = first_result.select_one("h3 > a")["href"]
    print("Title:", title)
    print("Link:", link)
else:
    print("No results found for", query)
