import pandas as pd
from pathlib import Path


REQUIRED_COLUMNS = ["student_id", "name", "age", "score"]


def clean_students(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    for col in REQUIRED_COLUMNS:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df = df.dropna(subset=["name"])
    df = df.drop_duplicates(subset=["student_id"])
    df["age"] = df["age"].astype(int)
    df["score"] = df["score"].astype(int)

    if ((df["score"] < 0) | (df["score"] > 100)).any():
        raise ValueError("Score out of range")

    return df


def run_etl(input_path="input_students.csv", output_path="output/cleaned_students.csv"):
    df = pd.read_csv(input_path)
    cleaned = clean_students(df)

    Path("output").mkdir(exist_ok=True)
    cleaned.to_csv(output_path, index=False)

    return cleaned


if __name__ == "__main__":
    run_etl()