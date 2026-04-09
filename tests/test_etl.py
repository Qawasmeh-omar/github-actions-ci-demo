import pandas as pd
import pytest
from pathlib import Path
from etl import clean_students, run_etl


def test_required_columns_exist():
    df = pd.DataFrame({
        "student_id": [1, 2],
        "name": ["Ali", "Sara"],
        "age": [20, 21],
        "score": [80, 90]
    })
    cleaned = clean_students(df)
    assert list(cleaned.columns) == ["student_id", "name", "age", "score"]


def test_missing_required_column():
    df = pd.DataFrame({
        "student_id": [1, 2],
        "name": ["Ali", "Sara"],
        "age": [20, 21]
    })
    with pytest.raises(ValueError, match="Missing required column: score"):
        clean_students(df)


def test_remove_null_names():
    df = pd.DataFrame({
        "student_id": [1, 2],
        "name": ["Ali", None],
        "age": [20, 21],
        "score": [80, 90]
    })
    cleaned = clean_students(df)
    assert len(cleaned) == 1


def test_remove_duplicates():
    df = pd.DataFrame({
        "student_id": [1, 1, 2],
        "name": ["Ali", "Ali", "Sara"],
        "age": [20, 20, 21],
        "score": [80, 80, 90]
    })
    cleaned = clean_students(df)
    assert len(cleaned) == 2


def test_score_range_invalid():
    df = pd.DataFrame({
        "student_id": [1],
        "name": ["Ali"],
        "age": [20],
        "score": [120]
    })
    with pytest.raises(ValueError, match="Score out of range"):
        clean_students(df)


def test_run_etl_creates_output():
    run_etl()
    output_file = Path("output/cleaned_students.csv")
    assert output_file.exists()


def test_output_has_rows():
    run_etl()
    df = pd.read_csv("output/cleaned_students.csv")
    assert len(df) > 0


def test_output_no_duplicate_ids():
    run_etl()
    df = pd.read_csv("output/cleaned_students.csv")
    assert df["student_id"].duplicated().sum() == 0