from pathlib import Path
import pandas as pd
from src.config.settings import RAW_JOBS_FILE


def read_raw_jobs_csv(file_path: Path = RAW_JOBS_FILE) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    return df
