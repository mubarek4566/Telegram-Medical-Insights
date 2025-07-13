-- fct_image_detections.sql
SELECT
    CAST(message_id AS INTEGER) AS message_id,
    detected_object_class,
    confidence_score,
    channel,
    image_path
FROM {{ ref('stg_image_detections') }}


with detections as (
    select *
    from {{ ref('stg_image_detections') }}
),

messages as (
    select *
    from {{ ref('fct_messages') }}
)

select
    m.message_id,
    d.channel,
    d.detected_object_class,
    d.confidence_score,
    d.image_path
from detections d
left join messages m
    on d.message_id = m.message_id
