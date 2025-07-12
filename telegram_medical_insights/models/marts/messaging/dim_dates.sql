-- models/marts/messaging/dim_dates.sql

with dates as (

    select generate_series(
        date '2023-01-01',
        current_date,
        interval '1 day'
    )::date as date_day

)

select
    date_day,
    extract(year from date_day)::int as year,
    extract(month from date_day)::int as month,
    extract(day from date_day)::int as day,
    to_char(date_day, 'Month') as month_name,
    to_char(date_day, 'Day') as day_name,
    extract(isodow from date_day)::int as day_of_week,
    extract(week from date_day)::int as week_of_year,
    date_day = current_date as is_today
from dates
