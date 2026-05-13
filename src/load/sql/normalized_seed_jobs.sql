INSERT INTO jobs (
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
SELECT DISTINCT
    jt.job_title_id,
    c.company_id,
    jl.location_id AS job_location_id,
    sl.location_id AS search_location_id,
    p.platform_id,
    st.schedule_type_id,
    sr.salary_rate_id,
    r.job_title,
    job_posted_date,
    COALESCE(r.job_work_from_home, FALSE),
    r.salary_year_avg,
    r.salary_hour_avg,
    COALESCE(r.job_no_degree_mention, FALSE),
    COALESCE(r.job_health_insurance, FALSE)
FROM public.raw_jobs AS r
LEFT JOIN job_titles AS jt
    ON jt.job_title_name = NULLIF(BTRIM(r.job_title_short), '')
LEFT JOIN companies AS c
    ON c.company_name = NULLIF(
        BTRIM(
            TRANSLATE(r.company_name, CHR(34), '')
        ),
        ''
    )
LEFT JOIN locations AS jl
    ON jl.raw_location = NULLIF(BTRIM(r.job_location), '')
LEFT JOIN locations AS sl
    ON sl.raw_location = NULLIF(BTRIM(r.search_location), '')
LEFT JOIN platforms AS p
    ON p.platform_name = CASE
        WHEN lower(BTRIM(r.job_via)) LIKE 'via %'
            THEN NULLIF(BTRIM(SUBSTRING(BTRIM(r.job_via) FROM 5)), '')
        ELSE NULLIF(BTRIM(r.job_via), '')
    END
LEFT JOIN schedule_types AS st
    ON st.schedule_type_name = NULLIF(BTRIM(r.job_schedule_type), '')
LEFT JOIN salary_rates AS sr
    ON sr.salary_rate_name = lower(NULLIF(BTRIM(r.salary_rate), ''))
WHERE NULLIF(BTRIM(r.job_title), '') IS NOT NULL;
