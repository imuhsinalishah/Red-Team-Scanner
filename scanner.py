import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import threading
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

class WebScanner:
    def __init__(self, base_url, depth=2, use_selenium=True, use_proxies=False):
        self.base_url = base_url.rstrip('/')  # Remove trailing slashes
        self.depth = depth
        self.visited_links = set()
        self.use_selenium = use_selenium
        self.use_proxies = use_proxies
        self.proxies = {"http": "http://your-proxy-ip:port", "https": "https://your-proxy-ip:port"}  # Replace with a real proxy
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        self.lock = threading.Lock()  # Ensures thread safety

        if self.use_selenium:
            self.driver = self.init_selenium()  # Initialize Selenium driver

    def init_selenium(self):
        """Initializes and configures Selenium WebDriver (Headless Chrome)."""
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Run in headless mode (no GUI)
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument(f"user-agent={self.headers['User-Agent']}")

        service = Service(ChromeDriverManager().install())  # Auto-download ChromeDriver
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver

    def send_request(self, url):
        """Fetches a web page using Selenium (if enabled) or requests."""
        try:
            if self.use_selenium:
                self.driver.get(url)
                time.sleep(2)  # Wait for JavaScript to load
                return self.driver.page_source  # Return full rendered HTML
            else:
                response = requests.get(url, headers=self.headers, proxies=self.proxies if self.use_proxies else None, timeout=5)
                response.raise_for_status()
                return response.text
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
            return None

    def extract_links(self, html):
        """Extracts and returns all internal links from a web page."""
        soup = BeautifulSoup(html, "html.parser")
        links = set()
        for anchor in soup.find_all("a", href=True):
            link = urljoin(self.base_url, anchor["href"])
            if link.startswith(self.base_url) and link not in self.visited_links:
                links.add(link)
        return links

    def crawl(self, url, depth):
        """Recursively crawls web pages up to a given depth (multi-threading enabled)."""
        if depth == 0 or url in self.visited_links:
            return

        with self.lock:  # Ensures thread safety
            print(f"[Crawling] {url}")
            self.visited_links.add(url)

        html = self.send_request(url)
        if html:
            links = self.extract_links(html)
            threads = []
            for link in links:
                thread = threading.Thread(target=self.crawl, args=(link, depth - 1))
                threads.append(thread)
                thread.start()
                time.sleep(1)  # Prevents overloading the server

            for thread in threads:
                thread.join()

    def save_results(self, filename="crawled_links.txt"):
        """Saves crawled links to a file."""
        with open(filename, "w") as file:
            for link in sorted(self.visited_links):
                file.write(link + "\n")
        print(f"[INFO] Results saved to {filename}")

    def close(self):
        """Closes the Selenium WebDriver (if used)."""
        if self.use_selenium:
            self.driver.quit()

if __name__ == "__main__":
    target_url = input("Enter target URL (e.g., https://example.com): ").strip()
    scanner = WebScanner(target_url, depth=2, use_selenium=True, use_proxies=False)
    scanner.crawl(target_url, depth=2)
    scanner.save_results()
    scanner.close()
    print(f"Visited {len(scanner.visited_links)} pages")
