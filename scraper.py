import os
import json
import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

KEYWORDS = ["edital", "processo seletivo", "admissão", "inscriç", "vagas", "mestrado", "doutorado", "ingresso"]

university_directory = [
    {"name": "UEA - Hematologia", "url": "https://posgraduacao.uea.edu.br/hematologia/", "state": "AM", "region": "Norte"},
    {"name": "UEA - Ciências Humanas", "url": "https://posgraduacao.uea.edu.br/cienciashumanas/", "state": "AM", "region": "Norte"},
    {"name": "UEA - PPGLETRAS", "url": "https://ppgla.uea.edu.br", "state": "AM", "region": "Norte"},
    {"name": "UEA - Portal Central", "url": "https://www.uea.edu.br/", "state": "AM", "region": "Norte"},
    {"name": "UESC - Central", "url": "https://uesc.br", "state": "BA", "region": "Nordeste"},
    {"name": "UESC - Produção Vegetal", "url": "https://ppgpv.uesc.br/pt/", "state": "BA", "region": "Nordeste"},
    {"name": "UFG - Computação", "url": "https://ppgcc.inf.ufg.br/", "state": "GO", "region": "Centro-Oeste"},
    {"name": "UnB - Letras/Linguística", "url": "https://pgla.unb.br/", "state": "DF", "region": "Centro-Oeste"},
    {"name": "UTFPR - Química", "url": "https://www.utfpr.edu.br/cursos/programas-de-pos-graduacao/ppgqb-td", "state": "PR", "region": "Sul"},
    {"name": "UFPR - Engenharia de Produção", "url": "http://www.ppgep.ufpr.br", "state": "PR", "region": "Sul"},
    {"name": "UFES - Engenharia Civil", "url": "https://engenhariacivil.ufes.br/pt-br/pos-graduacao/PPGEC", "state": "ES", "region": "Sudeste"},
    {"name": "UNIFESP - Educação", "url": "https://ppg.unifesp.br/educacao/en/", "state": "SP", "region": "Sudeste"}
]

def fetch_page_html(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=12, verify=False)
        return response.text if response.status_code == 200 else None
    except Exception as e:
        print(f"⚠️ Connection dropped for {url}: {e}")
        return None

def extract_academic_links(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    valid_discoveries = []
    for anchor in soup.find_all('a', href=True):
        href_url = anchor['href']
        text_context = anchor.get_text().strip().lower()
        if any(href_url.lower().endswith(ext) for ext in ['.pdf', '.zip', '.rar', '.docx', '.xlsx']):
            continue
        if any(keyword in text_context for keyword in KEYWORDS):
            full_link = href_url if href_url.startswith('http') else base_url.rstrip('/') + '/' + href_url.lstrip('/')
            valid_discoveries.append({"title": anchor.get_text().strip(), "link": full_link})
    return valid_discoveries

def analyze_program_status(link_url):
    html = fetch_page_html(link_url)
    if not html:
        return "Check Portal", "See Website"
    html_lower = html.lower()
    status = "Check Portal"
    if "inscrições abertas" in html_lower or "prorrogado" in html_lower:
        status = "Open"
    elif "encerrado" in html_lower or "inscrições encerradas" in html_lower:
        status = "Closed"
    return status, "See Website"

def run_scraper_engine():
    print(f"🚀 Initializing crawling matrix across {len(university_directory)} targets...")
    compiled_results = []
    uid = 1
    for uni in university_directory:
        print(f"Analyzing: {uni['name']} ({uni['state']})")
        page_content = fetch_page_html(uni['url'])
        if not page_content:
            continue
        found_links = extract_academic_links(page_content, uni['url'])
        if found_links:
            primary_discovery = found_links[0]
            status, deadline = analyze_program_status(primary_discovery['link'])
            compiled_results.append({
                "id": uid, "university": uni['name'], "program": primary_discovery['title'],
                "region": uni['region'], "state": uni['state'], "status": status, "deadline": deadline, "link": primary_discovery['link']
            })
            uid += 1
    with open("discovered_programs.json", "w", encoding="utf-8") as file:
        json.dump(compiled_results, file, ensure_ascii=False, indent=2)
    print("🎉 Run successful. Data mapped to discovered_programs.json")

if __name__ == '__main__':
    run_scraper_engine()
