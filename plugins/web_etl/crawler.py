import requests
import os
import yaml
from datetime import datetime

class WebsiteCrawler:
    def __init__(
        self,
        config_path="./config/website.yaml",
        raw_storage_path="./data/raw"
    ):
        self.raw_storage_path = raw_storage_path
        os.makedirs(self.raw_storage_path, exist_ok=True)

        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        self.websites = config.get("websites", [])

    def fetch_and_store(self):
        results = []

        for site in self.websites:
            name = site["name"]
            url = site["url"]

            try:
                response = requests.get(url, timeout=10)
                response.raise_for_status()

                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

                # Create website-specific folder (S3-like structure)
                site_folder = os.path.join(self.raw_storage_path, name)
                os.makedirs(site_folder, exist_ok=True)

                filename = f"{timestamp}.html"
                filepath = os.path.join(site_folder, filename)

                # Store raw HTML
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(response.text)

                print(f"Successfully crawled: {url}")
                results.append(filepath)

            except requests.RequestException as e:
                print(f"Failed to crawl {url}: {str(e)}")

        return results
