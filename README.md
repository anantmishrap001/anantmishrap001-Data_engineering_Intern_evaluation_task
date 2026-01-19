# Website Content Extraction Pipeline

**Data Engineer Intern – Evaluation Task (GrowthPal)**

---

## Project Overview

This project implements an **end-to-end data engineering pipeline** orchestrated using **Apache Airflow**.
The pipeline crawls company websites, stores raw HTML in an S3-style folder structure, extracts and standardizes key content sections using simple heuristics, and generates aggregated analytical metrics.

The implementation prioritizes **clean pipeline design, reliability, and clarity**, with a clear separation between orchestration and business logic.

---

## What the Pipeline Does

1. Crawls selected company websites and internal pages
2. Stores raw HTML and crawl metadata without modification
3. Extracts meaningful content sections:
   * Navbar
   * Homepage content
   * Footer
   * Case studies (if available)
4. Transforms extracted content into a standardized JSON schema
5. Generates aggregated analytics from processed data

---

## Data Workflow

```
Websites
   ↓
Raw HTML Storage (data/raw)
   ↓
Extracted & Standardized Records (data/processed)
   ↓
Aggregated Metrics (data/analytics)
```

Each stage produces deterministic outputs and can be re-run safely.

---

## Project Structure

```
├── dags/
│   └── website_content_dag.py      
├── plugins/
│   └── web_etl/
│       ├── crawler.py              
│       ├── extractor.py            
│       └── analytics.py            
├── data/
│   ├── raw/                        
│   ├── processed/                  
│   └── analytics/                  
└── requirements.txt
```

---

## Design Choices Implemented

**Separation of Concerns**

* Airflow DAG is limited to orchestration and dependencies
* Crawling, extraction, and analytics logic are implemented in modular Python files

**Raw Data Storage (S3 Simulation)**

* Raw HTML is stored unchanged in a structured directory layout
* Raw, processed, and analytics data are stored in separate layers

**Heuristic-Based Extraction**

* HTML is parsed using BeautifulSoup
* Semantic tags and keyword matching are used to identify sections
* Missing sections are captured as empty content and flagged inactive

**Idempotent Execution**

* Re-running the DAG overwrites outputs for the same inputs
* No duplicate data is created across runs

---

## Error Handling & Reliability

* HTTP requests use timeouts and exception handling
* Crawl failures for individual websites do not stop the pipeline
* Missing HTML sections do not cause task failures
* Airflow tasks are configured with retries and retry delays

---

## Data Model

Each processed record follows a consistent schema:

```json
{
  "website": "https://example.com",
  "section": "case_study",
  "content": "Extracted text...",
  "crawl_timestamp": "2026-01-19T10:30:00Z",
  "isActive": true
}
```

---

## Deliverables Included

* Airflow DAG defining task boundaries and execution order
* Python modules for crawling, extraction, and analytics
* Sample raw, processed, and aggregated data outputs
* Documentation explaining design decisions and reliability handling

---

## Evaluation Alignment

This project demonstrates:

* Clear data modeling and pipeline structure
* Reasonable and explainable extraction logic
* Well-defined Airflow DAG and task separation
* Robust error handling and logging
* Strong understanding of data engineering workflows and trade-offs

---

**Author:** Anant Mishra
**Role:** Data Engineer Intern Candidate
