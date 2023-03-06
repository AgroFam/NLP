from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time

# Define the URL of the documentation page
url = 'https://help.appdirect.com/'

# Set up a Selenium driver
driver = webdriver.Chrome()
driver.get(url)

# Find the search input field and enter a query
search_input = driver.find_element_by_id('searchInput')
search_input.send_keys('create product')
search_input.send_keys(Keys.RETURN)

# Wait for the search results to load
time.sleep(5)

# Parse the HTML of the search results page
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all instances of a specific tag or class that contains the keyword
results = soup.find_all('div', {'class': 'search-result'})
matches = [result for result in results if 'create product' in result.text]

# Define a function that takes a query and returns relevant results
def search_documentation(query):
    search_input = driver.find_element_by_id('searchInput')
    search_input.clear()
    search_input.send_keys(query)
    search_input.send_keys(Keys.RETURN)
    time.sleep(5)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    results = soup.find_all('div', {'class': 'search-result'})
    matches = [result for result in results if query in result.text]
    return matches

# Test the function with a sample query
query = 'create product'
results = search_documentation(query)
print(results)

# Close the Selenium driver
driver.quit()

