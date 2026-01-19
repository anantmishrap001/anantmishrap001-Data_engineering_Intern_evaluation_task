import requests
import os
from datetime import datetime
from urllib.parse import urlparse

class WebsiteCrawler:
    def __init__(self, raw_storage_path="./data/raw"):
        self.storage_path = raw_storage_path
        os.makedirs(self.storage_path, exist_ok=True)
        
        # Target websites (Scalable list)
        self.targets = [
            "https://www.python.org",
            "https://airflow.apache.org",
            "https://pandas.pydata.org",
            # Add more companies here to scale to n-companies
        ]

    def fetch_and_store(self):
        results = []
        for url in self.targets:
            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()
                
                domain = urlparse(url).netloc
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{domain}_{timestamp}.html"
                filepath = os.path.join(self.storage_path, filename)

                # Store raw HTML (Simulating S3 put_object)
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(response.text)
                
                print(f"Successfully crawled: {url}")
                results.append(filepath)
                
            except requests.RequestException as e:
                print(f"Failed to crawl {url}: {str(e)}")
                # In a real scenario, push this to a Dead Letter Queue (DLQ)
        
        return results