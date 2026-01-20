import os
import json
from bs4 import BeautifulSoup
from datetime import datetime

class ContentExtractor:
    def __init__(self, raw_path="./data/raw", processed_path="./data/processed"):
        self.raw_path = raw_path
        self.processed_path = processed_path
        os.makedirs(self.processed_path, exist_ok=True)

    def _extract_text(self, soup, tag, class_name=None):
        """Helper to safely extract text based on heuristics."""
        element = soup.find(tag, class_=class_name) if class_name else soup.find(tag)
        return element.get_text(strip=True) if element else ""

    def process_raw_files(self):
        # os.walk allows us to look into subdirectories created by your crawler
        for root, dirs, files in os.walk(self.raw_path):
            for file in files:
                if not file.endswith('.html'):
                    continue
                
                raw_filepath = os.path.join(root, file)
                
                # The 'name' of the website is the parent folder name
                domain = os.path.basename(root) 
                
                with open(raw_filepath, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Heuristic extraction logic
                case_study_keywords = ['case study', 'success stories', 'use cases', 'community']
                case_study_content = ""
                for keyword in case_study_keywords:
                    found_link = soup.find("a", string=lambda t: t and keyword in t.lower())
                    if found_link:
                        case_study_content = f"Found: {found_link.get('href')}"
                        break
                
                sections = {
                    "navbar": self._extract_text(soup, "nav") or self._extract_text(soup, "header"),
                    "footer": self._extract_text(soup, "footer"),
                    "homepage": self._extract_text(soup, "main") or self._extract_text(soup, "body"),
                    "case_study": case_study_content
                }

                # Save JSON records
                for section_name, content in sections.items():
                    record = {
                        "website": domain,
                        "section": section_name,
                        "content": content[:500],
                        "crawl_timestamp": datetime.now().isoformat(),
                        "isActive": bool(content)
                    }
                    
                    # Create unique name: domain_section.json
                    output_file = f"{domain}_{section_name}.json"
                    output_path = os.path.join(self.processed_path, output_file)
                    
                    with open(output_path, 'w', encoding='utf-8') as out:
                        json.dump(record, out, indent=2)