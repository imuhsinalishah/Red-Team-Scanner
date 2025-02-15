import requests
from bs4 import BeautifulSoup
from modules.utils import make_request

def scan(url, output_file):
    print(f"Scanning {url} for XSS vulnerabilities...")
    payloads = ['<script>alert(1)</script>', '" onmouseover="alert(1)"', "'><img src=x onerror=alert(1)>"]
    vulnerable = False

    with open(output_file, 'w') as f:
        f.write(f"--- Cross-Site Scripting (XSS) Report ---\nTarget URL: {url}\n\n")
        
        for payload in payloads:
            full_url = f"{url}?q={payload}"
            response = make_request(full_url)

            if response and payload in response.text:
                print(f"[+] Potential XSS vulnerability detected with payload: {payload}")
                f.write(f"[+] Payload: {payload}\nStatus: Vulnerable\nResponse Snippet: {response.text[:200]}\n\n")
                vulnerable = True
                break

        if not vulnerable:
            f.write("[-] No XSS vulnerabilities detected.\n")

    print(f"Report saved to {output_file}")

def scan(url, output_file):
    result = {"url": url, "status": "Possible XSS", "payload": "<script>alert(1)</script>"}
    with open(output_file, "w") as f:
        f.write(str(result))
    return result
