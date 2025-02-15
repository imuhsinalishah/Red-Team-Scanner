import requests
import random
import time
from fake_useragent import UserAgent

# Proxy list for evasion
proxies = [
    {"http": "http://127.0.0.1:8080", "https": "https://127.0.0.1:8080"},
    {"http": "http://your-proxy.com:3128", "https": "https://your-proxy.com:3128"}
]

# Security headers to check
security_headers = [
    "X-Frame-Options", "Content-Security-Policy", "Strict-Transport-Security",
    "X-Content-Type-Options", "Referrer-Policy"
]

def check_security_headers(url):
    # Random User-Agent spoofing
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    
    # Random Proxy selection
    proxy = random.choice(proxies)
    
    # Random delay to evade detection
    time.sleep(random.uniform(1, 5))
    
    try:
        response = requests.get(url, headers=headers, proxies=proxy, timeout=10)
        print(f"\nChecking security headers for {url}\n")
        
        for header in security_headers:
            if header in response.headers:
                print(f"[✔] {header}: {response.headers[header]}")
            else:
                print(f"[✖] {header} is MISSING!")
    
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")

# Example Usage
if __name__ == "__main__":
    target_url = input("Enter target URL: ")
    check_security_headers(target_url)
