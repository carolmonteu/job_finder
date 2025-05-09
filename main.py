from datetime import datetime
import os
from dotenv import load_dotenv
from modules.search import JobSearch
from modules.notification import Notifier
from modules.storage import JobStorage

def main():
    # Chargement de la configuration
    load_dotenv()
    
    # Initialisation des modules
    search = JobSearch(config_path="config/")
    notifier = Notifier()
    storage = JobStorage(results_dir=os.getenv("RESULTS_DIR", "./job_results"))
    
    # Exécution de la recherche
    results = []
    for query in search.generate_queries():
        for result in search.google_search(query, os.getenv("SERPAPI_KEY")):
            content = search.scrape_job_page(result.get("link", ""))
            if content:
                results.append({
                    "title": result.get("title", ""),
                    "url": result.get("link", ""),
                    "content": content[:500],
                    "date": datetime.now().strftime("%Y-%m-%d")
                })
    
    # Sauvegarde et notification
    if results:
        filename = storage.save_results(results)
        notifier.send(f"{len(results)} nouvelles offres trouvées", 
                     enabled=os.getenv("NOTIFICATION_ENABLED") == "true")

if __name__ == "__main__":
    main()