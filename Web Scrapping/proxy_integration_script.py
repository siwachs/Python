# Scrape multiple pages of a target website while avoiding IP blocks by implementing a proxy rotation mechanism.
import requests
import random
from itertools import cycle


def generate_mock_proxy():
    protocal = random.choice(['http', 'https'])
    ip_address = '.'.join(str(random.randint(0, 255)) for _ in range(4))
    port = random.randint(1000, 9999)
    return f"{protocal}://{ip_address}:{port}"


TARGET_URL = 'https://mangatoon.mobi'
PROXY_LIST = [generate_mock_proxy() for _ in range(1)]

# Set headers (optional but recommended to mimic a real browser)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# Create Iterator to Iterate Proxy
proxyPool = cycle(PROXY_LIST)


def make_request(url):
    while True:
        if (len(PROXY_LIST) == 0):
            print("All proxies are invalid please provide a new list.")
            break
        proxy = next(proxyPool)
        try:
            response = requests.get(
                url, proxies={'http': proxy, 'https': proxy}, headers=headers)
            if response.status_code == 200:
                return response.text
        except Exception as e:
            print(f"Can not connect to {proxy} Error: {e}")
            PROXY_LIST.remove(proxy)


noOfPagesToScrape = 3

for pageNumber in range(1, noOfPagesToScrape + 1):
    pageURL = f"{TARGET_URL}/en/genre/comic?page={pageNumber}"
    htmlContent = make_request(pageURL)
    print(f"Content Scrapped from page: {pageNumber}")
    print(htmlContent)
