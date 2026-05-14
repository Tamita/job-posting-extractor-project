INSERT INTO job_skills (job_id, skill_id)
SELECT DISTINCT
    j.job_id,
    s.skill_id
FROM public.raw_jobs AS r
CROSS JOIN LATERAL jsonb_array_elements_text(
    r.job_skills::jsonb
) AS raw_skill(skill_name)
JOIN jobs AS j
    ON j.raw_job_id = r.raw_job_id
JOIN skills AS s
    ON s.skill_name = lower(NULLIF(BTRIM(raw_skill.skill_name), ''))
WHERE r.job_skills IS NOT NULL
  AND NULLIF(BTRIM(raw_skill.skill_name), '') IS NOT NULL
ON CONFLICT (job_id, skill_id) DO NOTHING;
