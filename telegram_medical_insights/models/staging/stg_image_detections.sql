{{ config(materialized='view') }}

with source as (
    select
        message_id,
        detected_object_class,
        confidence_score,
        channel,
        image_path
    from {{ source('raw', 'image_detections') }}
),

final as (
    select
        cast(message_id as integer) as message_id,
        detected_object_class,
        cast(confidence_score as float) as confidence_score,
        channel,
        image_path
    from source
)

select * from final
