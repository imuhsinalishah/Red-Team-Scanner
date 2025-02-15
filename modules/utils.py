import requests
import random

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

PROXIES = {
    "http": "http://127.0.0.1:8080",  # Replace with your proxy (e.g., Burp Suite)
    "https": "http://127.0.0.1:8080"
}

def make_request(url):
    headers = {'User-Agent': random.choice(USER_AGENTS)}
    try:
        response = requests.get(url, headers=headers, proxies=PROXIES, timeout=5)
        return response
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return None
