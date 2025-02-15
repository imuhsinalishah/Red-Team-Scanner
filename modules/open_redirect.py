import requests
from urllib.parse import urljoin, urlencode

def scan(url, output_file):
    print(f"Scanning {url} for Open Redirect vulnerabilities...")
    payloads = [
        "http://evil.com",
        "//evil.com",
        "/\\evil.com",
        "///evil.com",
        "http:evil.com"
    ]
    vulnerable = False

    with open(output_file, 'w') as f:
        f.write(f"--- Open Redirect Report ---\nTarget URL: {url}\n\n")

        for payload in payloads:
            redirect_param = {'next': payload}
            full_url = f"{url}?{urlencode(redirect_param)}"

            try:
                response = requests.get(full_url, allow_redirects=False)
                if response.status_code in [300, 301, 302, 307, 308]:
                    location_header = response.headers.get('Location', '')
                    if 'evil.com' in location_header:
                        print(f"[+] Potential Open Redirect detected with payload: {payload}")
                        f.write(f"[+] Payload: {payload}\nRedirects to: {location_header}\nStatus: Vulnerable\n\n")
                        vulnerable = True
                        break
            except Exception as e:
                print(f"Error occurred: {e}")
                f.write(f"Error: {e}\n")

        if not vulnerable:
            f.write("[-] No Open Redirect vulnerabilities detected.\n")
def scan(url, output_file):
    result = {"url": url, "status": "Possible Open Redirect", "payload": "https://evil.com"}
    with open(output_file, "w") as f:
        f.write(str(result))
    return result
