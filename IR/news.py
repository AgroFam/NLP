import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/searchImage')
def google_search():
    query = request.args.get("q"," ")
    print("Searching for:", query)

    # Set the base URL for the Google search
    base_url = "https://www.google.com/search?q={}&num=10"

    # Set the headers to avoid detection as a bot
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }

    # Define a function to retrieve and parse search results for a given URL
    def retrieve_search_results(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select("div.g")
        results = []
        for result in search_results:
            title = result.select_one("h3").get_text()
            link = result.select_one("a")["href"]
            results.append({"title": title, "link": link})
        return results

    # Create a thread pool with 5 workers
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Generate a list of URLs for each page of search results
        urls = [base_url.format(query) + "&start=" + str(i) for i in range(1, 51, 10)]
        # Submit a task for each URL to retrieve and parse search results
        results = executor.map(retrieve_search_results, urls)
        # Flatten the results into a single list
        flattened_results = [result for sublist in results for result in sublist]

    # Return the search results as a JSON response
    return jsonify({"results": flattened_results})

if __name__ == '__main__':
    app.run()

