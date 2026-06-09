import json
import time
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.google.com/"
}

TARGET_KEYWORDS = ["mestrado", "doutorado", "pos-graduacao", "edital", "processo-seletivo", "ingresso"]

def fetch_page_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            return response.text
        else:
            print(f"⚠️ Skipped: {url} returned Status Code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Network Error connecting to {url}: {e}")
        return None

def extract_academic_links(html_content, base_url):
    soup = BeautifulSoup(html_content, 'html.parser')
    found_links = []
    for anchor in soup.find_all('a', href=True):
        link_text = anchor.get_text(strip=True).lower()
        href_url = anchor['href']
        full_url = urljoin(base_url, href_url)
        if urlparse(full_url).netloc != urlparse(base_url).netloc:
            continue
        if any(keyword in link_text or keyword in href_url.lower() for keyword in TARGET_KEYWORDS):
            if full_url not in [item['link'] for item in found_links]:
                found_links.append({
                    "title": anchor.get_text(strip=True),
                    "link": full_url
                })
    return found_links

def run_pipeline(target_universities):
    scraped_database = []
    print("🚀 Starting Automated Discovery Pipeline...\n")
    for uni in target_universities:
        print(f"🔍 Inspecting: {uni['name']} ({uni['url']})")
        html = fetch_page_html(uni['url'])
        if html:
            discovered = extract_academic_links(html, uni['url'])
            print(f"✅ Found {len(discovered)} relevant links on this page.")
            scraped_database.append({
                "university": uni["name"],
                "state": uni["state"],
                "region": uni["region"],
                "discovered_links": discovered
            })
        delay = random.uniform(2.0, 4.0)
        time.sleep(delay)
        print("-" * 40)

    with open('discovered_programs.json', 'w', encoding='utf-8') as f:
        json.dump(scraped_database, f, ensure_ascii=False, indent=4)

    print("\n💾 Pipeline complete. Data saved to 'discovered_programs.json'")

if __name__ == "__main__":
    test_university_list = [
        {"name": "UEA (Univ. do Estado do Amazonas)", "url": "https://posgraduacao.uea.edu.br/", "state": "AM", "region": "Norte"},
        {"name": "UFC (Univ. Federal do Ceará)", "url": "http://www.prppg.ufc.br/", "state": "CE", "region": "Nordeste"}
    ]
    run_pipeline(test_university_list)
