# Website Content Extraction Pipeline

---

## Project Overview

This project demonstrates a **basic end-to-end data engineering pipeline** built using **Python and Apache Airflow**.

The pipeline:

* Visits company websites
* Stores raw website HTML files
* Extracts useful content sections
* Converts the content into a structured format
* Generates simple analytics

The main goal of this project is to show **clear data flow, good structure, and reliable execution**, rather than advanced web scraping.

---

## What This Project Does

The pipeline performs the following steps:

1. Crawls company websites and internal pages
2. Saves raw HTML files without changing them
3. Extracts important sections such as:

   * Navbar
   * Homepage content
   * Footer
   * Case studies (if present)
4. Converts extracted content into a standard JSON format
5. Creates summary analytics from the processed data

---

## Data Workflow

```
Websites
   ↓
Raw HTML Files (data/raw)
   ↓
Structured JSON Data (data/processed)
   ↓
Analytics Output (data/analytics)
```

Each step runs independently and can be safely re-run.

---

## Project Structure

```
├── dags/
│   └── website_content_dag.py      # Airflow DAG defining the pipeline schedule & tasks
│
├── plugins/
│   └── web_etl/
│       ├── crawler.py              # Downloads website HTML
│       ├── extractor.py            # Extracts structured content from HTML
│       └── analytics.py            # Computes analytics from processed data
│
├── config/
│   └── websites.yaml               #stores website names
│
├── data/
│   ├── raw/                        # Raw downloaded HTML files
│   ├── processed/                  # Cleaned & structured JSON data
│   └── analytics/                  # Analytics results
│
├── Docker-compose.yaml             # Docker setup (likely for Airflow + service)
├── README.md                      # Project documentation & overview
├── .gitignore
└── requirements.txt               # Python dependencies


```

---

## Design Choices Made

### Separation of Tasks

* Airflow handles **only the workflow order**
* Python files handle **actual processing logic**

This makes the code easier to read and debug.

---

### Raw Data Storage

* Website HTML is stored exactly as downloaded
* Raw data is kept separate from processed data

This allows reprocessing without re-downloading websites.

---

### Simple Content Extraction

* HTML is parsed using **BeautifulSoup**
* Common HTML tags and keywords are used to find sections
* Missing sections are handled safely without errors

---

### Idempotent Pipeline

* Running the pipeline multiple times does not create duplicates
* Output files are overwritten with the latest results

---

## Error Handling

* Network requests use timeouts
* Errors from one website do not stop the entire pipeline
* Missing HTML sections are marked inactive instead of failing
* Airflow retries tasks automatically if a temporary error occurs

---

## Data Format

Each processed record follows this structure:

```json
{
  "website": "https://example.com",
  "section": "case_study",
  "content": "Extracted text...",
  "crawl_timestamp": "2026-01-19T10:30:00Z",
  "isActive": true
}
```

**Author:** Anant Mishra
**Role:** Data Engineer Intern Candidate
