from dagster import job, op
import subprocess
import os
set PYTHONLEGACYWINDOWSSTDIO=true


@op
def scrape_telegram_data():
    os.system("python scripts/telegram_scraper.py")
    print("✅ Telegram data scraped.")

@op
def load_raw_to_postgres():
    from scripts.load_json_to_postgres import load_json_data_main
    load_json_data_main()
    print("✅ Raw JSON data loaded into PostgreSQL.")

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], check=True)
    print("✅ dbt transformations completed.")

@op
def run_yolo_enrichment():
    from scripts.object_detection import run_object_detection
    from scripts.load_json_to_postgres import load_image_predictions

    run_object_detection()
    load_image_predictions()
    print("✅ YOLO enrichment pipeline completed.")

@job
def telegram_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
