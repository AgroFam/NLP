import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request
from urllib.parse import urlparse

app = Flask(__name__)

# Setting user-agent header to avoid detection as a bot
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

# Google search URL with query and number of results
base_url = "https://www.google.com/search?q={}&num=10"

@app.route("/news")
def news():
    # Get the query from the request args
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400
    
    # Create a function to retrieve search results for a single page
    def retrieve_search_results(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select("div.g")
        results = []
        for result in search_results:
            title = result.select_one("h3").get_text()
            link = result.select_one("a")["href"]
            
            # Check if the link is a valid URL
            try:
                response = requests.get(link, headers=headers)
                response.raise_for_status()
                parsed_link = urlparse(link)._asdict()
                
                # Check if the link has an image preview
                img_url = None
                img_preview = result.select_one("img")
                if img_preview:
                    img_url = img_preview.get("src")
                    # Check if the image URL is relative and convert to absolute
                    if not bool(urlparse(img_url).netloc):
                        img_url = f"{parsed_link['scheme']}://{parsed_link['netloc']}/{img_url.lstrip('/')}"
                
                # Create a link preview object
                link_preview = {
                    "title": title,
                    "url": link,
                    "domain": parsed_link["netloc"],
                    "img_url": img_url
                }
                results.append(link_preview)
                
            except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError):
                continue
        
        return results

    # Create a thread pool with 5 workers
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Generate a list of URLs for each page of search results
        urls = [base_url.format(query) + "&start=" + str(i) for i in range(1, 11, 10)]
        # Submit a task for each URL to retrieve and parse search results
        results = executor.map(retrieve_search_results, urls)
        # Flatten the results into a single list and sort by image presence
        flattened_results = sorted([result for sublist in results for result in sublist], key=lambda x: bool(x["img_url"]), reverse=True)
        
    return jsonify({"results": flattened_results})

if __name__ == '__main__':
    app.run()
