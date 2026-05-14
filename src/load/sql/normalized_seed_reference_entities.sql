INSERT INTO companies (company_name)
SELECT DISTINCT cleaned_company_name
FROM (
    SELECT NULLIF(
        BTRIM(
            TRANSLATE(company_name, CHR(34), '')
        ),
        ''
    ) AS cleaned_company_name
    FROM public.raw_jobs
    WHERE company_name IS NOT NULL
) companies_source
WHERE cleaned_company_name IS NOT NULL
  AND lower(cleaned_company_name) NOT IN ('unknown', 'n/a', 'na', 'null', '-')
ON CONFLICT (company_name) DO NOTHING;

INSERT INTO platforms (platform_name)
SELECT DISTINCT
    CASE
        WHEN lower(BTRIM(job_via)) LIKE 'via %'
            THEN NULLIF(BTRIM(SUBSTRING(BTRIM(job_via) FROM 5)), '')
        ELSE NULLIF(BTRIM(job_via), '')
    END AS platform_name
FROM public.raw_jobs
WHERE NULLIF(BTRIM(job_via), '') IS NOT NULL
ON CONFLICT (platform_name) DO NOTHING;

INSERT INTO schedule_types (schedule_type_name)
SELECT DISTINCT NULLIF(BTRIM(job_schedule_type), '')
FROM public.raw_jobs
WHERE NULLIF(BTRIM(job_schedule_type), '') IS NOT NULL
ON CONFLICT (schedule_type_name) DO NOTHING;

INSERT INTO salary_rates (salary_rate_name)
SELECT DISTINCT lower(NULLIF(BTRIM(salary_rate), ''))
FROM public.raw_jobs
WHERE NULLIF(BTRIM(salary_rate), '') IS NOT NULL
ON CONFLICT (salary_rate_name) DO NOTHING;

INSERT INTO job_titles (job_title_name)
SELECT DISTINCT NULLIF(BTRIM(job_title_short), '')
FROM public.raw_jobs
WHERE NULLIF(BTRIM(job_title_short), '') IS NOT NULL
ON CONFLICT (job_title_name) DO NOTHING;
