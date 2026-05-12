from .data_extractor import read_raw_jobs_csv

def run_pipeline() -> None:
    df = read_raw_jobs_csv()
    print(df.head())
