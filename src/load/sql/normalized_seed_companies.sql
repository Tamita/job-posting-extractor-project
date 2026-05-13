INSERT INTO companies (company_name)
SELECT DISTINCT cleaned_name
FROM (
    SELECT NULLIF(REGEXP_REPLACE(BTRIM(company_name), '\s+', ' ', 'g'), '') AS cleaned_name
    FROM public.raw_jobs
    WHERE company_name IS NOT NULL
) t
WHERE cleaned_name IS NOT NULL
ON CONFLICT (company_name) DO NOTHING;
