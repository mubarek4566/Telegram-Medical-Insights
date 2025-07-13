-- Fail if any message has no text and no media
SELECT *
FROM {{ ref('stg_telegram_messages') }}
WHERE text IS NULL
  AND has_media IS FALSE;
