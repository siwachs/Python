# 4)Scrape multiple pages of a target website while avoiding IP blocks by implementing a proxy rotation mechanism.
import requests
import random
from itertools import cycle


def generate_mock_proxy():
    protocol = random.choice(['http', 'https'])
    ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    port = random.randint(1000, 9999)
    return f"{protocol}://{ip_address}:{port}"


TARGET_URL = 'https://mangatoon.mobi'
PROXY_LIST = [generate_mock_proxy()
              for _ in range(3)]  # Generate 3 mock proxies

# Set headers to mimic a real browser
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# Create an iterator to iterate over the proxy list
proxyPool = cycle(PROXY_LIST)


def make_request(url):
    while True:
        if not PROXY_LIST:
            print("All proxies are invalid. Please provide a new list.")
            break
        proxy = next(proxyPool)
        try:
            response = requests.get(
                url, proxies={'http': proxy, 'https': proxy}, headers=headers)
            if response.status_code == 200:
                return response.text
        except requests.RequestException as e:
            print(f"Could not connect to {proxy}. Error: {e}")
            PROXY_LIST.remove(proxy)


no_of_pages_to_scrape = 3

for page_number in range(1, no_of_pages_to_scrape + 1):
    page_url = f"{TARGET_URL}/en/genre/comic?page={page_number}"
    html_content = make_request(page_url)
    print(f"Content scraped from page: {page_number}")
    print(html_content)
