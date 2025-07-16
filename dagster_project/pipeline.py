# dagster_project/pipeline.py

from dagster import job, op, schedule, get_dagster_logger
import subprocess

@op
def scrape_telegram_data():
    logger = get_dagster_logger()
    logger.info("📥 Scraping Telegram data...")
    subprocess.run(["python", "scripts/telegram_scraper.py"], check=True)
    logger.info("✅ Scraping completed")

@op
def load_raw_to_postgres():
    logger = get_dagster_logger()
    logger.info("🗃️ Loading raw JSON to Postgres...")
    subprocess.run(["python", "scripts/load_json_to_postgres.py"], check=True)
    logger.info("✅ Loading completed")

@op
def run_dbt_transformations():
    logger = get_dagster_logger()
    logger.info("🏗️ Running dbt transformations...")
    subprocess.run(["dbt", "run", "--select", "dim_channels", "dim_dates", "fct_messages"], check=True)
    logger.info("✅ dbt models built")

@op
def run_yolo_enrichment():
    logger = get_dagster_logger()
    logger.info("🧠 Running YOLO object detection...")
    subprocess.run(["python", "scripts/object_detection.py"], check=True)
    logger.info("✅ YOLO detections complete")

    logger.info("⬆️ Loading image detections to Postgres...")
    subprocess.run(["python", "scripts/load_json_to_postgres.py", "--load-detections"], check=True)
    logger.info("✅ Enrichment data loaded")

@job
def telegram_pipeline_job():
    # Define pipeline sequence
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()

# Schedule: every day at 6 AM (Addis Ababa time)
@schedule(
    cron_schedule="0 6 * * *",
    job=telegram_pipeline_job,
    execution_timezone="Africa/Addis_Ababa",
)
def daily_telegram_pipeline_schedule():

# ✅ Daily schedule at 6 AM
daily_telegram_pipeline_schedule = ScheduleDefinition(
    job=telegram_pipeline_job,
    cron_schedule="0 6 * * *",  # Every day at 6:00 AM
    name="daily_telegram_pipeline_schedule",
)