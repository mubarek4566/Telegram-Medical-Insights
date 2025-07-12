-- models/marts/messaging/dim_channels.sql

with source as (
    select distinct channel
    from {{ ref('stg_telegram_messages') }}
)

select
    {{ dbt_utils.generate_surrogate_key(['channel']) }} as channel_id,
    channel
from source
