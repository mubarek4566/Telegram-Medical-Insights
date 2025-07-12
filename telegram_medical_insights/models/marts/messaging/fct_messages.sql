-- models/marts/messaging/fct_messages.sql

with messages as (
    select
        {{ dbt_utils.generate_surrogate_key(['channel']) }} as channel_id,
        cast(message_id as integer) as message_id,
        cast(message_date as date) as message_date,
        has_media,
        media_type,
        length(coalesce(message_text, '')) as message_length,
        case when media_type = 'MessageMediaPhoto' then true else false end as has_image
    from {{ ref('stg_telegram_messages') }}
)

select
    message_id,
    channel_id,
    message_date,
    has_media,
    has_image,
    message_length
from messages
