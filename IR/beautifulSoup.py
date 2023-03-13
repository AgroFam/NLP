import requests
from bs4 import BeautifulSoup

query = input("Enter your query: ")
print("Searching for:", query)

# URL for the Google search
url = f"https://www.google.com/search?q={query}&num=10"

# Setting user-agent header to avoid detection as a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Sending request to Google search and retrieving HTML content
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# Extracting search results
search_results = soup.select("div.g")
    
if len(search_results) > 0:
    # Extracting and printing the first search result
    first_result = search_results[0]
    second_result = search_results[1]
    title = first_result.select_one("h3").get_text()
    link = first_result.select_one("a")["href"]
    link2 = second_result.select_one("a")["href"]
    print("Title:", title)
    print("Link:", link)
    print("Link:", link2)
else:
    print("No results found for", query)
