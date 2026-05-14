INSERT INTO jobs (
    raw_job_id,
    job_title_id,
    company_id,
    job_location_id,
    search_location_id,
    platform_id,
    schedule_type_id,
    salary_rate_id,
    job_title,
    job_posted_date,
    job_work_from_home,
    salary_year_avg,
    salary_hour_avg,
    job_no_degree_mention,
    job_health_insurance
)
SELECT
    raw_jobs.raw_job_id,
    job_titles.job_title_id,
    companies.company_id,
    job_location.location_id AS job_location_id,
    search_location.location_id AS search_location_id,
    platforms.platform_id,
    schedule_types.schedule_type_id,
    salary_rates.salary_rate_id,
    NULLIF(BTRIM(raw_jobs.job_title), '') AS job_title,
    raw_jobs.job_posted_date,
    COALESCE(raw_jobs.job_work_from_home, false),
    raw_jobs.salary_year_avg,
    raw_jobs.salary_hour_avg,
    COALESCE(raw_jobs.job_no_degree_mention, false),
    COALESCE(raw_jobs.job_health_insurance, false)
FROM public.raw_jobs AS raw_jobs
LEFT JOIN job_titles
    ON job_titles.job_title_name = NULLIF(BTRIM(raw_jobs.job_title_short), '')
LEFT JOIN companies
    ON companies.company_name = NULLIF(BTRIM(raw_jobs.company_name), '')
LEFT JOIN locations AS job_location
    ON job_location.raw_location = NULLIF(BTRIM(raw_jobs.job_location), '')
LEFT JOIN locations AS search_location
    ON search_location.raw_location = NULLIF(BTRIM(raw_jobs.search_location), '')
LEFT JOIN platforms
    ON platforms.platform_name = CASE
        WHEN lower(BTRIM(raw_jobs.job_via)) LIKE 'via %'
            THEN NULLIF(BTRIM(SUBSTRING(BTRIM(raw_jobs.job_via) FROM 5)), '')
        ELSE NULLIF(BTRIM(raw_jobs.job_via), '')
    END
LEFT JOIN schedule_types
    ON schedule_types.schedule_type_name = NULLIF(BTRIM(raw_jobs.job_schedule_type), '')
LEFT JOIN salary_rates
    ON salary_rates.salary_rate_name = lower(NULLIF(BTRIM(raw_jobs.salary_rate), ''))
WHERE NULLIF(BTRIM(raw_jobs.job_title), '') IS NOT NULL
ON CONFLICT (raw_job_id) DO NOTHING;
