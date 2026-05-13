INSERT INTO locations (
    raw_location,
    city,
    state,
    country
)
SELECT DISTINCT
    cleaned_location AS raw_location,
    CASE
        WHEN array_length(location_parts, 1) = 3 THEN NULLIF(BTRIM(location_parts[1]), '')
        WHEN array_length(location_parts, 1) = 2 THEN NULLIF(BTRIM(location_parts[1]), '')
        ELSE NULL
    END AS city,
    CASE
        WHEN array_length(location_parts, 1) = 3 THEN NULLIF(BTRIM(location_parts[2]), '')
        ELSE NULL
    END AS state,
    CASE
        WHEN array_length(location_parts, 1) = 3 THEN NULLIF(BTRIM(location_parts[3]), '')
        WHEN array_length(location_parts, 1) = 2 THEN NULLIF(BTRIM(location_parts[2]), '')
        ELSE NULL
    END AS country
FROM (
    SELECT
        cleaned_location,
        string_to_array(cleaned_location, ',') AS location_parts
    FROM (
        SELECT DISTINCT NULLIF(BTRIM(job_location), '') AS cleaned_location
        FROM public.raw_jobs
        WHERE NULLIF(BTRIM(job_location), '') IS NOT NULL
    ) raw_locations
) parsed_locations
ON CONFLICT (raw_location) DO NOTHING;
