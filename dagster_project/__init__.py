# dagster_project/__init__.py

from dagster import Definitions
from dagster_project.pipeline import telegram_pipeline_job
from dagster_project.schedules import daily_telegram_pipeline_schedule

defs = Definitions(
    jobs=[telegram_pipeline_job],
    schedules=[daily_telegram_pipeline_schedule]
)
