# ==================== INTRODUCTION ====================
# Requests is an elegant HTTP library for Python
# Installation:
# pip install requests

import requests
from bs4 import BeautifulSoup
import urllib.request
import urllib.parse

# ==================== GET REQUEST ====================
print("\n=== GET REQUEST ===")

url = "https://www.example.com"
try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Check for HTTP errors
    print("Status code:", response.status_code)  # Should be 200
except requests.exceptions.Timeout:
    print("Timeout occurred (expected in demo)")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")

# ==================== HTTP STATUS CODES ====================
print("\n=== STATUS CODES ===")

status_url = "https://httpbin.org/status/404"
response = requests.get(status_url)
print(f"Status {response.status_code}: {'Success' if response.ok else 'Error'}")

# Status code categories:
# 2XX - Success
# 3XX - Redirection 
# 4XX - Client Errors
# 5XX - Server Errors

# ==================== REQUEST CONTENT ====================
print("\n=== CONTENT ===")

response = requests.get("https://www.example.com")
print("HTML content length:", len(response.content))  # Raw bytes
print("Text content length:", len(response.text))    # Decoded string

# ==================== POST REQUEST ==================== 
print("\n=== POST REQUEST ===")

post_url = "https://httpbin.org/post"
data = {"name": "Salah", "message": "Hello!"}

response = requests.post(post_url, json=data)
print("Response JSON:", response.json())

# ==================== ERROR HANDLING ====================
print("\n=== ERROR HANDLING ===")

error_url = "https://httpbin.org/status/404"
response = requests.get(error_url)

if not response.ok:
    print(f"Error {response.status_code}: Request failed")

# Better error handling with try/except
try:
    response = requests.get("https://non-existent-url.com")
    response.raise_for_status()  # Raises exception for 4XX/5XX
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP error: {http_err}")
except requests.exceptions.RequestException as err:
    print(f"Request error: {err}")

# ==================== TIMEOUTS ====================
print("\n=== TIMEOUTS ===")

timeout_url = "https://httpbin.org/delay/3"

try:
    response = requests.get(timeout_url, timeout=2)
    print("Request succeeded!")
except requests.exceptions.Timeout:
    print("Request timed out")

# ==================== HEADERS ====================
print("\n=== HEADERS ===")

headers_url = "https://httpbin.org/headers"
headers = {
    "User-Agent": "MyApp/1.0",
    "Accept": "application/json"
}

response = requests.get(headers_url, headers=headers)
print("Response headers:", response.json()['headers'])

# ==================== WEB SCRAPING ====================
print("\n=== WEB SCRAPING ===")

scrape_url = "https://www.example.com"
try:
    response = requests.get(scrape_url, timeout=5)
    response.raise_for_status()  # Check for HTTP errors
    soup = BeautifulSoup(response.content, "html.parser")

    title = soup.title.string if soup.title else "No title"
    first_paragraph = soup.p.get_text() if soup.p else "No paragraph"
    links = [a.get('href') for a in soup.find_all('a')]

    print(f"Title: {title}")
    print(f"First paragraph: {first_paragraph[:50]}...")
    print(f"Found {len(links)} links")
except requests.exceptions.Timeout:
    print("Timeout occurred (expected in demo)")
except requests.exceptions.RequestException as e:
    print(f"Request failed: {e}")
except Exception as e:
    print(f"Scraping failed: {e}")

# ==================== REQUESTS VS URLLIB ====================
print("\n=== REQUESTS VS URLLIB ===")

# Requests (easier)
data = {"key": "value"}
response = requests.post("https://httpbin.org/post", json=data)
print("Requests response:", response.json())

# Urllib (more verbose)
data = urllib.parse.urlencode({"key": "value"}).encode("utf-8")
req = urllib.request.Request("https://httpbin.org/post", data=data, method="POST")
try:
    with urllib.request.urlopen(req, timeout=5) as response:  # Increased timeout
        print("Urllib response:", response.read().decode())
except urllib.error.URLError as e:
    if isinstance(e.reason, TimeoutError):
        print("Urllib timeout occurred! Consider increasing the timeout.")
    else:
        print("Urllib error:", e)

""" 
=== COMPARISON ===
Feature        Requests        Urllib
Ease of Use    🟢 Excellent    🔴 Verbose
JSON Support   🟢 Built-in     🔴 Manual
Timeout        🟢 Simple       🔴 Complex
Headers        🟢 Easy         🔴 Manual
SSL            🟢 Automatic    🔴 Manual
"""

# ==================== BEST PRACTICES ====================
"""
1. Always use try/except blocks
2. Set reasonable timeouts
3. Check status codes with response.ok or response.raise_for_status()
4. Use sessions for multiple requests to the same host
5. Respect robots.txt and website terms of service
6. Add delays between requests when scraping
"""
