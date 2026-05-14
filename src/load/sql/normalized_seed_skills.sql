-- 1. Insert skill types from job_type_skills keys
INSERT INTO skill_types (skill_type_name)
SELECT DISTINCT skill_type_name
FROM (
    SELECT lower(NULLIF(BTRIM(skill_type_key), '')) AS skill_type_name
    FROM (
        SELECT jsonb_object_keys(job_type_skills::jsonb) AS skill_type_key
        FROM public.raw_jobs
        WHERE job_type_skills IS NOT NULL
    ) skill_type_keys
) cleaned_skill_types
WHERE skill_type_name IS NOT NULL
ON CONFLICT (skill_type_name) DO NOTHING;


-- 2. Insert skills with their related skill_type_id
INSERT INTO skills (skill_name, skill_type_id)
SELECT DISTINCT
    cleaned_skills.skill_name,
    skill_types.skill_type_id
FROM (
    SELECT
        lower(NULLIF(BTRIM(skill_type_entry.key), '')) AS skill_type_name,
        lower(NULLIF(BTRIM(skill_entry.value), '')) AS skill_name
    FROM public.raw_jobs
    CROSS JOIN LATERAL jsonb_each(
        COALESCE(job_type_skills::jsonb, '{}'::jsonb)
    ) AS skill_type_entry(key, value)
    CROSS JOIN LATERAL jsonb_array_elements_text(
        CASE
            WHEN jsonb_typeof(skill_type_entry.value) = 'array'
                THEN skill_type_entry.value
            ELSE '[]'::jsonb
        END
    ) AS skill_entry(value)
    WHERE job_type_skills IS NOT NULL
) cleaned_skills
INNER JOIN skill_types
    ON skill_types.skill_type_name = cleaned_skills.skill_type_name
WHERE cleaned_skills.skill_name IS NOT NULL
  AND cleaned_skills.skill_type_name IS NOT NULL
ON CONFLICT (skill_name) DO NOTHING;
