import requests
from bs4 import BeautifulSoup
import json
import os
import datetime
import re
from urllib.parse import quote_plus

# Configuration améliorée
SERPAPI_KEY = "84fc046b59c0d7ef7332ffcc86918090e0d9103580daa80846d6ab0e7ac8de3b"
KEYWORDS = [
    "analyste cybersécurité", "pentester", "ethical hacker", "soc analyst",
    "siem", "security consultant", "cybersecurity remote", "cybersecurity douala",
    "consultant sécurité informatique", "administrateur sécurité", "spécialiste sécurité"
]
LOCATIONS = ["douala", "cameroun", "remote", "télétravail", "afrique"]

# Liste étendue de sites de recherche d'emploi et entreprises locales
JOB_SITES = [
    "linkedin.com/jobs", "indeed.com", "jobartis.com", "emploi.cm",
    "africajob.com", "jobberman.com", "fnecm.org", "akwajobs.com",
    "africtech.com", "camerjob.com", "doucarmetal.com", "mtn.cm/carrieres",
    "orange-cameroun.com", "afrilandfirstbank.com", "ecobank.com"
]

# Entreprises locales à cibler
LOCAL_COMPANIES = [
    "mtn.cm", "orange-cameroun.com", "afrilandfirstbank.com", "ecobank.com",
    "express-exchange.com", "doucarmetal.com", "cimencam.com", "societegenerale.cm",
    "nestsolutions.com", "nexttechnology.cm"
]

DATE = datetime.datetime.now().strftime("%Y-%m-%d")
RESULTS_DIR = "job_results"
FILENAME = f"{RESULTS_DIR}/cyber_jobs_{DATE}.json"
os.makedirs(RESULTS_DIR, exist_ok=True)

def send_notification(message):
    try:
        if os.name == 'posix':  # Linux/Mac
            os.system(f'notify-send "🛡️ CyberJob Notifier" "{message}"')
        elif os.name == 'nt':  # Windows
            from win10toast import ToastNotifier
            toast = ToastNotifier()
            toast.show_toast("CyberJob Notifier", message, duration=10)
        else:
            print(f"[!] Notification: {message}")
    except Exception as e:
        print(f"[-] Erreur de notification: {e}")

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def google_search(query):
    print(f"[+] Recherche Google : {query}")
    params = {
        "api_key": SERPAPI_KEY,
        "engine": "google",
        "q": query,
        "hl": "fr",
        "gl": "cm",
        "num": 20
    }
    try:
        resp = requests.get("https://serpapi.com/search", params=params)
        resp.encoding = 'utf-8'
        data = resp.json()
        results = []
        for result in data.get("organic_results", []):
            link = result.get("link", "")
            title = result.get("title", "")
            snippet = result.get("snippet", "")
            
            if (any(kw.lower() in title.lower() for kw in KEYWORDS) and \
               (any(loc.lower() in snippet.lower() for loc in LOCATIONS))):
                results.append({
                    "title": title,
                    "url": link,
                    "source": "Google SERP",
                    "date": DATE
                })
        return results
    except Exception as e:
        print(f"[-] Erreur SERPAPI: {str(e)}")
        return []

def scrape_job_page(url):
    print(f"[>] Scraping : {url}")
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "fr-FR,fr;q=0.9"
        }
        r = requests.get(url, timeout=15, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")
        text = ' '.join(soup.stripped_strings).lower()
        
        has_keywords = any(kw in text for kw in KEYWORDS)
        has_location = any(loc in text for loc in LOCATIONS)
        
        if has_keywords and has_location:
            return {
                "url": url,
                "content_snippet": ' '.join(text.split()[:500]),
                "location": "Douala" if "douala" in text else ("Remote" if "remote" in text or "télétravail" in text else "Non précisé")
            }
    except Exception as e:
        print(f"[-] Échec scraping {url} : {str(e)}")
    return None

def generate_queries():
    queries = []
    for kw in KEYWORDS:
        site_query = f"{kw} site:" + " OR site:".join(JOB_SITES)
        queries.append(site_query)
        company_query = f"{kw} site:" + " OR site:".join(LOCAL_COMPANIES)
        queries.append(company_query)
    
    queries.extend([
        '"offre d\'emploi" +cybersécurité +douala',
        '"recrutement" +"sécurité informatique" +cameroun',
        '"poste vacant" +pentest +remote'
    ])
    return queries

def run_search():
    results = []
    queries = generate_queries()
    
    for query in queries:
        try:
            google_links = google_search(query)
            for entry in google_links:
                scraped = scrape_job_page(entry["url"])
                if scraped:
                    results.append({
                        "title": entry["title"],
                        "url": entry["url"],
                        "snippet": scraped["content_snippet"],
                        "location": scraped["location"],
                        "date_scraped": DATE,
                        "keywords": [kw for kw in KEYWORDS if kw in entry["title"].lower()]
                    })
        except Exception as e:
            print(f"[-] Erreur lors du traitement de la requête {query}: {str(e)}")
            continue

    if results:
        save_to_json(results, FILENAME)
        print(f"[+] {len(results)} résultats enregistrés dans {FILENAME}")
        send_notification(f"{len(results)} nouvelles offres détectées!")
    else:
        print("[-] Aucun résultat pertinent trouvé.")

if __name__ == "__main__":
    run_search()