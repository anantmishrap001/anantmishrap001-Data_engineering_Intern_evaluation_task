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
        files = [f for f in os.listdir(self.raw_path) if f.endswith('.html')]
        
        for file in files:
            raw_filepath = os.path.join(self.raw_path, file)
            
            with open(raw_filepath, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            soup = BeautifulSoup(html_content, 'html.parser')
                        
            # We look for ANY link containing these keywords
            case_study_keywords = ['case study', 'success stories', 'use cases', 'community', 'blog']
            case_study_content = ""
            
            # Find the first link that matches any keyword
            for keyword in case_study_keywords:
                found_link = soup.find("a", string=lambda t: t and keyword in t.lower())
                if found_link:
                    case_study_content = f"Found section '{keyword}': {found_link.get('href')}"
                    break 
            
            sections = {
                "navbar": self._extract_text(soup, "nav") or self._extract_text(soup, "header"),
                "footer": self._extract_text(soup, "footer"),
                "homepage": self._extract_text(soup, "main") or self._extract_text(soup, "body"),
                "case_study": case_study_content
            }
            # Create Standardized Records
            base_filename = file.replace('.html', '')
            domain = base_filename.split('_')[0]
            
            for section_name, content in sections.items():
                record = {
                    "website": f"https://{domain}",
                    "section": section_name,
                    "content": content[:500], # Keep truncation to keep files small
                    "crawl_timestamp": datetime.now().isoformat(),
                    "isActive": bool(content)
                }
                
                output_file = f"{base_filename}_{section_name}.json"
                output_path = os.path.join(self.processed_path, output_file)
                
                with open(output_path, 'w', encoding='utf-8') as out:
                    json.dump(record, out, indent=2)