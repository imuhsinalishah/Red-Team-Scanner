# Web Exploitation Tool

## Purpose
This tool identifies SQL Injection and Cross-Site Scripting (XSS) vulnerabilities in web applications.

## Features
- SQL Injection detection
- Cross-Site Scripting detection
- Proxy and User-Agent rotation for stealth
- Detailed report generation
- Open Redirect Detection

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/usman2ki/Web_Exploitation_Tool.git
   cd web_exploit_tool

or 

create a python virtual environment to run python script


## Usage
Run the tool with the following options:

- **SQL Injection Scan**:
  ```bash
  python webexploit.py --url <target_url> --scan sqli --output <path_to_report>
  python webexploit.py --url <target_url> --scan xss --output <path_to_report>
  python webexploit.py --url <target_url> --scan redirect --output <path_to_report>

## Example
python webexploit.py --url http://testphp.vulnweb.com/redirect.php --scan redirect --output reports\redirect_report.txt
