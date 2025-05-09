import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote_plus
from datetime import datetime

class JobSearch:
    def __init__(self, config_path="config/"):
        self.load_config(config_path)
        
    def load_config(self, config_path):
        with open(f"{config_path}sites.json") as f:
            sites_config = json.load(f)
            self.job_sites = sites_config["job_sites"]
            self.local_companies = sites_config["local_companies"]
            
        with open(f"{config_path}keywords.json") as f:
            keywords_config = json.load(f)
            self.keywords = keywords_config["keywords"]
            self.locations = keywords_config["locations"]

    def google_search(self, query, api_key):
        params = {
            "api_key": api_key,
            "engine": "google",
            "q": query,
            "hl": "fr",
            "gl": "cm",
            "num": 20
        }
        try:
            resp = requests.get("https://serpapi.com/search", params=params)
            resp.encoding = 'utf-8'
            return resp.json().get("organic_results", [])
        except Exception as e:
            print(f"Search error: {e}")
            return []

    def scrape_job_page(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept-Language": "fr-FR,fr;q=0.9"
            }
            # Timeout ajustable (15s pour la connexion, 30s pour la lecture)
            r = requests.get(url, timeout=(15, 30), headers=headers)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, "html.parser")
            text = ' '.join(soup.stripped_strings).lower()
            return text
        except Exception as e:
            print(f"Scraping error for {url}: {str(e)}")
            return ""
    

    def generate_queries(self):
        queries = []
        for kw in self.keywords:
            site_query = f"{kw} site:" + " OR site:".join(self.job_sites)
            queries.append(site_query)
            company_query = f"{kw} site:" + " OR site:".join(self.local_companies)
            queries.append(company_query)
        return queries