-- models/staging/stg_telegram_messages.sql

with source as (
    select * 
    from {{ source('raw', 'telegram_messages') }}
),

renamed as (
    select
        cast(message_id as integer) as message_id,
        channel,
        cast(text as text) as message_text,
        has_media,
        media_type,
        cast(date as timestamp) as message_date
    from source
)

select * from renamed
