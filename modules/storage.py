import json
import os
from datetime import datetime

class JobStorage:
    def __init__(self, results_dir):
        self.results_dir = results_dir
        os.makedirs(results_dir, exist_ok=True)

    def save_results(self, data):
        filename = f"{self.results_dir}/jobs_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return filename