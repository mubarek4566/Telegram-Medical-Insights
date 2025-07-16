# dagster_project/schedules.py

from dagster import ScheduleDefinition
from dagster_project.pipeline import telegram_pipeline_job

daily_telegram_pipeline_schedule = ScheduleDefinition(
    job=telegram_pipeline_job,
    cron_schedule="0 6 * * *",  # ⏰ runs every day at 6 AM
    execution_timezone="Africa/Addis_Ababa",  # Set your timezone
    name="daily_telegram_pipeline_schedule"
)
