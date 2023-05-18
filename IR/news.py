
# import requests
# from bs4 import BeautifulSoup
# from concurrent.futures import ThreadPoolExecutor
# from flask import Flask, jsonify, request

# app = Flask(__name__)

# @app.route("/searchWeb")
# def google_search():
#     query = request.args.get("q", "")
#     if not query:
#         return jsonify({"error": "No query provided"})
#     base_url = "https://www.google.com/search?q={}&num=10"

#     headers = {
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
#     }

#     def retrieve_search_results(url):
#         try:
#             response = requests.get(url, headers=headers)
#             response.raise_for_status()
#             soup = BeautifulSoup(response.text, "html.parser")
#             search_results = soup.select("div.g")
#             results = []
#             for result in search_results:
#                 try:
#                     # title = result.select_one("h1:is(h1, h2, h3, h4, h5, h6), h2:is(h1, h2, h3, h4, h5, h6), h3:is(h1, h2, h3, h4, h5, h6), h4:is(h1, h2, h3, h4, h5, h6), h5:is(h1, h2, h3, h4, h5, h6), h6:is(h1, h2, h3, h4, h5, h6)").get_text()
#                     title = result.select_one("h3").get_text()
#                     link = result.select_one("a")["href"]
#                     image = result.select_one("img")
#                     if image:
#                         image_url = image.get("src")
#                     else:
#                         image_url = None
#                     title_element = result.select_one("h1, h2, h3, h4, h5, h6")
#                     if title_element:
#                         title = title_element.get_text()
#                     else:
#                         title = None
#                     link = result.select_one("a")["href"]
#                     results.append({"title": title, "link": link, "image_url": image_url})

#                 except Exception as e:
#                     print(f"Error: {e}")
#             return results
#         except requests.exceptions.RequestException as e:
#             print(f"Error: {e}")
#             return []

#     with ThreadPoolExecutor(max_workers=5) as executor:
#         urls = [base_url.format(query) + "&start=" + str(i) for i in range(1, 101, 10)]
#         results = executor.map(retrieve_search_results, urls)
#         flattened_results = [result for sublist in results for result in sublist]

#     # Sort the search results with images first
#     sorted_results = sorted(flattened_results, key=lambda x: x["image_url"] is not None, reverse=True)
#     return jsonify({"results": sorted_results})

# if __name__ == '__main__':
#     app.run()


import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/searchWeb")
def google_search():
    query = request.args.get("q", "")
    if not query:
        return jsonify({"error": "No query provided"})
    base_url = "https://www.google.com/search?q={}&num=20"

    headers = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
    }

    try:
        response = requests.get(base_url.format(query), headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.select("div.g")
        results = []
        for result in search_results:
            try:
                title = result.select_one("h1:is(h1, h2, h3, h4, h5, h6), h2:is(h1, h2, h3, h4, h5, h6), h3:is(h1, h2, h3, h4, h5, h6), h4:is(h1, h2, h3, h4, h5, h6), h5:is(h1, h2, h3, h4, h5, h6), h6:is(h1, h2, h3, h4, h5, h6)").get_text()

                # title = result.select_one("h3").get_text()
                link = result.select_one("a")["href"]
                image = result.select_one("img")
                if image:
                    image_url = image.get("src")
                else:
                    image_url = None
                if not any(domain in link for domain in ["facebook.com", "twitter.com", "instagram.com"]):
                    results.append({"title": title, "link": link, "image_url": image_url})
            except Exception as e:
                print(f"Error: {e}")
        return jsonify({"results": results})
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return jsonify({"error": "Failed to retrieve search results"})

if __name__ == '__main__':
    app.run()