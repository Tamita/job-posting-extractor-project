WITH parsed_job_skills AS (
    SELECT DISTINCT
        lower(BTRIM(skill_value)) AS skill_name
    FROM public.raw_jobs r,
    LATERAL jsonb_array_elements_text(COALESCE(r.job_skills::jsonb, '[]'::jsonb)) AS skill_value
    WHERE NULLIF(BTRIM(skill_value), '') IS NOT NULL
),
parsed_job_type_skills AS (
    SELECT DISTINCT
        lower(BTRIM(skill_value)) AS skill_name,
        lower(BTRIM(skill_type_key)) AS skill_type_name
    FROM public.raw_jobs r,
    LATERAL jsonb_each(COALESCE(r.job_type_skills::jsonb, '{}'::jsonb)) AS typed_skills(skill_type_key, skill_array),
    LATERAL jsonb_array_elements_text(skill_array) AS skill_value
    WHERE NULLIF(BTRIM(skill_value), '') IS NOT NULL
      AND NULLIF(BTRIM(skill_type_key), '') IS NOT NULL
),
all_skills AS (
    SELECT skill_name
    FROM parsed_job_skills
    UNION
    SELECT skill_name
    FROM parsed_job_type_skills
)
INSERT INTO skills (skill_name)
SELECT skill_name
FROM all_skills
ON CONFLICT (skill_name) DO NOTHING;

WITH parsed_job_type_skills AS (
    SELECT DISTINCT
        lower(BTRIM(skill_value)) AS skill_name,
        lower(BTRIM(skill_type_key)) AS skill_type_name
    FROM public.raw_jobs r,
    LATERAL jsonb_each(COALESCE(r.job_type_skills::jsonb, '{}'::jsonb)) AS typed_skills(skill_type_key, skill_array),
    LATERAL jsonb_array_elements_text(skill_array) AS skill_value
    WHERE NULLIF(BTRIM(skill_value), '') IS NOT NULL
      AND NULLIF(BTRIM(skill_type_key), '') IS NOT NULL
)
INSERT INTO skill_type_skills (
    skill_id,
    skill_type_id
)
SELECT DISTINCT
    s.skill_id,
    st.skill_type_id
FROM parsed_job_type_skills pts
JOIN skills s
    ON s.skill_name = pts.skill_name
JOIN skill_types st
    ON st.skill_type_name = pts.skill_type_name
ON CONFLICT (skill_id, skill_type_id) DO NOTHING;
