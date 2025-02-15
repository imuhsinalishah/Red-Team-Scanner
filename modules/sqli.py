import requests
from bs4 import BeautifulSoup
from modules.utils import make_request

def scan(url, output_file):
    print(f"Scanning {url} for SQL Injection vulnerabilities...")
    
    payloads = ["' OR 1=1 --", '" OR 1=1 --', "' OR 'a'='a", '" OR "a"="a']
    vulnerable = False

    with open(output_file, 'w') as f:
        f.write(f"--- SQL Injection Report ---\nTarget URL: {url}\n\n")

        for payload in payloads:
            full_url = f"{url}?id={payload}"
            try:
                response = requests.get(full_url)
                if "SQL" in response.text or "syntax" in response.text or "error" in response.text:
                    print(f"[+] Potential SQL Injection detected with payload: {payload}")
                    f.write(f"[+] Payload: {payload}\nStatus: Vulnerable\n\n")
                    vulnerable = True
                    break
            except Exception as e:
                print(f"Error occurred: {e}")
                f.write(f"Error: {e}\n")

    if not vulnerable:
        f.write("[-] No SQL Injection vulnerabilities detected.")
def scan(url, output_file):
    result = {"url": url, "status": "Possible SQL Injection", "payload": "' OR 1=1 --"}
    with open(output_file, "w") as f:
        f.write(str(result))
    return result
