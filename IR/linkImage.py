# GIves image link as well along with search result and sorted in order such that result with image are shown above

import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, jsonify, request

app = Flask(__name__)

# Setting user-agent header to avoid detection as a bot
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# }

@app.route("/searchImage")
def get_news():
    query = request.args.get("q","")
    if not query:
        return jsonify({"error": "No query provided"})
    base_url = "https://www.google.com/search?q={}&num=10"

    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    def retrieve_search_results(url):
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select("div.g")
        results = []
        for result in search_results:
            title = result.select_one("h3").get_text()
            link = result.select_one("a")["href"]
            image = result.select_one("img")
            if image:
                image_url = image.get("src")
            else:
                image_url = None
            results.append({"title": title, "link": link, "image_url": image_url})
        return results

# @app.route("/searchImage")
# def get_news():
#     query = request.args.get("q","")
#     if not query:
#         return jsonify({"error": "No query provided"})
#     base_url = "https://www.google.com/search?q={}&num=10"
    with ThreadPoolExecutor(max_workers=5) as executor:
        urls = [base_url.format(query) + "&start=" + str(i) for i in range(1, 51, 10)]
        results = executor.map(retrieve_search_results, urls)
        flattened_results = [result for sublist in results for result in sublist]
    # Sort the search results with images first
    sorted_results = sorted(flattened_results, key=lambda x: x["image_url"] is not None, reverse=True)
    return jsonify({"results": sorted_results})

if __name__ == '__main__':
    app.run()

