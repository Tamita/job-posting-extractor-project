CREATE TABLE IF NOT EXISTS locations (
    location_id SERIAL PRIMARY KEY,
    raw_location TEXT UNIQUE,
    city TEXT,
    state TEXT,
    country TEXT
);

CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    company_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS platforms (
    platform_id SERIAL PRIMARY KEY,
    platform_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS schedule_types (
    schedule_type_id SERIAL PRIMARY KEY,
    schedule_type_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS salary_rates (
    salary_rate_id SERIAL PRIMARY KEY,
    salary_rate_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS job_titles (
    job_title_id SERIAL PRIMARY KEY,
    job_title_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS skill_types (
    skill_type_id SERIAL PRIMARY KEY,
    skill_type_name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS skills (
    skill_id SERIAL PRIMARY KEY,
    skill_name TEXT NOT NULL UNIQUE,
    skill_type_id INT NOT NULL REFERENCES skill_types(skill_type_id)
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    raw_job_id BIGINT UNIQUE,
    job_title_id INT REFERENCES job_titles(job_title_id),
    company_id INT REFERENCES companies(company_id),
    job_location_id INT REFERENCES locations(location_id),
    search_location_id INT REFERENCES locations(location_id),
    platform_id INT REFERENCES platforms(platform_id),
    schedule_type_id INT REFERENCES schedule_types(schedule_type_id),
    salary_rate_id INT REFERENCES salary_rates(salary_rate_id),
    job_title TEXT NOT NULL,
    job_posted_date TIMESTAMP,
    job_work_from_home BOOLEAN DEFAULT FALSE,
    salary_year_avg DECIMAL(12, 2),
    salary_hour_avg DECIMAL(12, 2),
    job_no_degree_mention BOOLEAN DEFAULT FALSE,
    job_health_insurance BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS job_skills (
    job_id INT NOT NULL REFERENCES jobs(job_id),
    skill_id INT NOT NULL REFERENCES skills(skill_id),
    CONSTRAINT pk_job_skills PRIMARY KEY (job_id, skill_id)
);

CREATE INDEX IF NOT EXISTS idx_jobs_raw_job_id
    ON jobs (raw_job_id);

CREATE INDEX IF NOT EXISTS idx_jobs_job_title_id
    ON jobs (job_title_id);

CREATE INDEX IF NOT EXISTS idx_jobs_company_id
    ON jobs (company_id);

CREATE INDEX IF NOT EXISTS idx_jobs_job_location_id
    ON jobs (job_location_id);

CREATE INDEX IF NOT EXISTS idx_jobs_search_location_id
    ON jobs (search_location_id);

CREATE INDEX IF NOT EXISTS idx_jobs_platform_id
    ON jobs (platform_id);

CREATE INDEX IF NOT EXISTS idx_jobs_schedule_type_id
    ON jobs (schedule_type_id);

CREATE INDEX IF NOT EXISTS idx_jobs_salary_rate_id
    ON jobs (salary_rate_id);

CREATE INDEX IF NOT EXISTS idx_skills_skill_type_id
    ON skills (skill_type_id);

CREATE INDEX IF NOT EXISTS idx_job_skills_skill_id
    ON job_skills (skill_id);
