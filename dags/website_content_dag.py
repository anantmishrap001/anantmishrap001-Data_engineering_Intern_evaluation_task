from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add plugins to path so Airflow can find our custom modules
sys.path.append(os.path.join(os.environ.get('AIRFLOW_HOME', '/opt/airflow'), 'plugins'))

from web_etl.crawler import WebsiteCrawler
from web_etl.extractor import ContentExtractor
from web_etl.analytics import DataAggregator

default_args = {
    'owner': 'data_intern',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# [cite_start]Define DAG [cite: 19]
with DAG(
    'website_content_pipeline_v1',
    default_args=default_args,
    description='Crawl, process, and analyze website content',
    schedule_interval='@daily',
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['etl', 'scraping'],
) as dag:

    # Task 1: Crawl Websites
    # Note: Wrappers are used to instantiate classes within the execution context
    def run_crawler():
        crawler = WebsiteCrawler()
        crawler.fetch_and_store()

    t1_crawl = PythonOperator(
        task_id='crawl_websites',
        python_callable=run_crawler,
        doc_md="Fetches HTML from target list and saves to data/raw"
    )

    # Task 2: Extract and Standardize
    def run_extractor():
        extractor = ContentExtractor()
        extractor.process_raw_files()

    t2_extract = PythonOperator(
        task_id='extract_and_tag',
        python_callable=run_extractor,
        doc_md="Reads raw HTML, parses sections using heuristics, saves JSON"
    )

    # Task 3: Aggregate Metrics
    def run_analytics():
        aggregator = DataAggregator()
        aggregator.generate_metrics()

    t3_aggregate = PythonOperator(
        task_id='aggregate_metrics',
        python_callable=run_analytics,
        doc_md="Reads processed JSONs and generates summary statistics"
    )

    # [cite_start]Define Dependencies [cite: 19]
    t1_crawl >> t2_extract >> t3_aggregate