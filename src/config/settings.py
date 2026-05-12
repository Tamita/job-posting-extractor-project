from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DATA_DIR = PROJECT_ROOT / "job-posting-extractor-project"
BRONZE_DIR = DATA_DIR / "data/bronze"
RAW_JOBS_FILE = BRONZE_DIR / "data_jobs.csv"
