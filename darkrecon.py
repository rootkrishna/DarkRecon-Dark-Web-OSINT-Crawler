import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from colorama import Fore, Style
import os

# Tor proxy config
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

# Save crawled URLs
visited = set()
output_file = "output.txt"

def save_link(url):
    with open(output_file, "a") as f:
        f.write(url + "\n")

def is_onion(url):
    return ".onion" in urlparse(url).netloc

def crawl(url, depth=2):
    if depth == 0 or url in visited or not is_onion(url):
        return

    print(Fore.CYAN + f"[+] Crawling: {url}" + Style.RESET_ALL)
    visited.add(url)
    save_link(url)

    try:
        response = requests.get(url, proxies=proxies, timeout=10)
        if 'text/html' not in response.headers.get('Content-Type', ''):
            return

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            full_url = urljoin(url, link['href'])
            if is_onion(full_url):
                crawl(full_url, depth - 1)

    except Exception as e:
        print(Fore.RED + f"[!] Error: {e}" + Style.RESET_ALL)

def banner():
    os.system("cls" if os.name == "nt" else "clear")
    print(Fore.GREEN + """
  _____             _     _____                      
 |  __ \           | |   |  __ \                     
 | |  | | ___ _ __ | |_  | |__) |___  ___ ___  _ __  
 | |  | |/ _ \ '_ \| __| |  _  // _ \/ __/ _ \| '_ \ 
 | |__| |  __/ | | | |_  | | \ \  __/ (_| (_) | | | |
 |_____/ \___|_| |_|\__| |_|  \_\___|\___\___/|_| |_|                             
         DarkRecon | .onion OSINT Crawler
         by KRISHNA ⚔️
""" + Style.RESET_ALL)

if __name__ == "__main__":
    banner()
    start_url = input(Fore.YELLOW + "Enter .onion URL to crawl: " + Style.RESET_ALL).strip()
    crawl(start_url, depth=2)
    print(Fore.GREEN + f"\n[✔] Crawling complete. Links saved to {output_file}" + Style.RESET_ALL)
