# GitHub Actions CI/CD Demo

A minimal app for demonstrating a CI pipeline with GitHub Actions.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows
pip install -r requirements.txt
pytest
python app.py
```

Open http://127.0.0.1:5000/

## GitHub Actions

# GitHub Actions CI/CD Demo

A BSc-level teaching repository for demonstrating how **CI/CD pipelines** can automatically verify:

- application functionality,
- API/request behavior,
- environment/configuration correctness,
- ETL/data quality,
- output file generation,
- packaging and artifacts.

This repo is designed to help students see that **CI/CD is not only about deployment**.  
It is also about **quality control, repeatability, and automated verification**.

---

# Learning Objectives

By using this repository, students should be able to:

- understand the role of CI/CD in software engineering,
- explain how GitHub Actions automates testing,
- distinguish between application testing and data/ETL testing,
- understand how environment variables can be validated,
- see how CI/CD can stop faulty changes before release.

---

# Main Idea

This repository demonstrates an important engineering principle:

> A CI/CD pipeline is a sequence of automated quality gates.  
> A change should only move forward if it passes the required checks.

---

# Repository Structure

```text
github-actions-ci-demo/
│   app.py
│   etl.py
│   requirements.txt
│   pytest.ini
│   input_students.csv
│   README.md
│   .gitignore
│
├── output/
│
├── tests/
│   ├── test_app.py
│   └── test_etl.py
│
└── .github/
    └── workflows/
        └── ci.yml
```

---

# Project Components

## `app.py`
A small Flask application used to demonstrate API-related CI/CD testing.

It includes endpoints such as:

- `/` → homepage
- `/health` → system health endpoint
- `/config` → checks whether an environment variable exists
- `/grade` → accepts a score and returns pass/fail

### What students learn from this part
- how to test web routes,
- how to validate requests,
- how to test business logic,
- how CI/CD can check configuration behavior.

---

## `etl.py`
A small ETL/data-cleaning script used to demonstrate data-engineering quality checks.

It performs tasks such as:

- reading a CSV file,
- validating required columns,
- removing null names,
- removing duplicate student IDs,
- converting columns to the correct type,
- validating score ranges,
- writing cleaned output to `output/cleaned_students.csv`.

### What students learn from this part
- how CI/CD can test ETL logic,
- how to validate data quality automatically,
- how to verify generated outputs,
- how CI/CD applies to DataOps, not only software apps.

---

## `tests/test_app.py`
Contains automated tests for the Flask application.

These tests verify:
- routes,
- invalid routes,
- configuration behavior,
- valid/invalid request handling,
- grading logic.

---

## `tests/test_etl.py`
Contains automated tests for the ETL workflow.

These tests verify:
- required columns,
- missing-column errors,
- null removal,
- duplicate removal,
- valid score ranges,
- output file creation,
- output file correctness.

---

## `.github/workflows/ci.yml`
Defines the GitHub Actions CI pipeline.

It performs:
1. checkout
2. Python setup
3. dependency installation
4. ETL execution
5. automated testing
6. packaging
7. artifact upload

---

# Setup Instructions

## 1. Clone the repository

```bash
git clone https://github.com/Qawasmeh-omar/github-actions-ci-demo.git
cd YOUR-REPO
```

---

## 2. Create a virtual environment

### Windows PowerShell
```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Run tests locally

```bash
pytest
```

If everything is correct, you should see something like:

```text
12 passed
```

The number may vary depending on how many tests exist.

---

## 5. Run the ETL script locally

```bash
python etl.py
```

This should generate:

```text
output/cleaned_students.csv
```

---

## 6. Run the Flask app locally

```bash
python app.py
```

Then open in your browser:

- `http://127.0.0.1:5000/`
- `http://127.0.0.1:5000/health`

---

# Why We Use `pytest`

`pytest` is a Python testing framework used to automatically verify that code behaves as expected.

In this repository, it is used to check:

- whether application endpoints return the correct output,
- whether invalid requests are handled properly,
- whether required environment variables exist,
- whether ETL logic behaves correctly,
- whether output files are created and valid.

## Why it matters in CI/CD
In the pipeline:

- if tests pass → the change can continue,
- if tests fail → the pipeline stops.

That makes tests a **quality gate**.

---

# CI Pipeline Overview

The GitHub Actions workflow runs automatically when:

- code is pushed to `main`,
- or a pull request targets `main`.

## Pipeline steps
1. **Checkout repository**
2. **Set up Python**
3. **Install dependencies**
4. **Run ETL**
5. **Run tests with pytest**
6. **Package project**
7. **Upload artifacts**

## Educational meaning
This shows students that CI/CD is a **repeatable automated verification workflow**.

---

# Example GitHub Actions Workflow

```yaml
name: CI Pipeline Demo

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build-test-package:
    runs-on: ubuntu-latest

    env:
      APP_MODE: ci

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run ETL
        run: python etl.py

      - name: Run tests
        run: pytest

      - name: Package project
        run: zip -r student-portal-demo.zip . -x "*.git*" "*__pycache__*" "*.pytest_cache*" "*.venv*"

      - name: Upload artifact
        uses: actions/upload-artifact@v4
        with:
          name: student-portal-demo
          path: |
            student-portal-demo.zip
            output/cleaned_students.csv
```

---

# Test Categories in This Repository

This repository is meant to show students that CI/CD can test multiple engineering layers.

---

## 1. Application Tests

These tests check whether the software behaves correctly.

### Examples
- homepage returns correct text,
- health route returns correct JSON,
- unknown route returns `404`.

### Why this matters
It shows that CI/CD can verify software behavior automatically.

---

## 2. Request Validation Tests

These tests check whether the API handles valid and invalid requests correctly.

### Examples
- valid score returns `"pass"` or `"fail"`,
- missing score returns `400`,
- invalid score type returns `400`,
- out-of-range score returns `400`.

### Why this matters
It shows that CI/CD can verify input validation and API correctness.

---

## 3. Configuration Tests

These tests check whether required configuration is available.

### Example
- `/config` works when `APP_MODE` exists,
- `/config` fails when `APP_MODE` is missing.

### Why this matters
It shows that CI/CD can validate environment setup, not just code.

---

## 4. ETL / Data Quality Tests

These tests check the correctness of the ETL workflow.

### Examples
- required columns must exist,
- null names must be removed,
- duplicate student IDs must be removed,
- score must be between 0 and 100,
- numeric columns must be valid.

### Why this matters
It shows that CI/CD can be used in data engineering and DataOps.

---

## 5. Output / Artifact Tests

These tests check whether the project generates the correct outputs.

### Examples
- cleaned CSV file exists,
- cleaned CSV file contains rows,
- cleaned CSV file has no duplicate student IDs.

### Why this matters
It shows that pipelines can verify final outputs, not only intermediate logic.

---

# Example Application Code

## `app.py`

```python
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.get("/")
def home():
    return "Student Portal CI/CD Demo"


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.get("/config")
def config_check():
    app_mode = os.getenv("APP_MODE")
    if not app_mode:
        return jsonify({"error": "APP_MODE is not set"}), 500
    return jsonify({"app_mode": app_mode})


@app.post("/grade")
def grade():
    data = request.get_json()

    if not data or "score" not in data:
        return jsonify({"error": "score is required"}), 400

    score = data["score"]

    if not isinstance(score, (int, float)):
        return jsonify({"error": "score must be numeric"}), 400

    if score < 0 or score > 100:
        return jsonify({"error": "score out of range"}), 400

    result = "pass" if score >= 50 else "fail"
    return jsonify({"result": result})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

---

# Example ETL Code

## `etl.py`

```python
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
```

---

# Example Input File

## `input_students.csv`

```csv
student_id,name,age,score
1,Ali,20,85
2,Sara,21,91
2,Sara,21,91
3,,19,70
4,Omar,22,45
```

This file intentionally contains:
- a duplicate ID,
- a missing name.

This allows the ETL tests to demonstrate cleaning behavior.

---

# Example Application Tests

## `tests/test_app.py`

```python
from app import app


def test_home_route():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Student Portal CI/CD Demo" in response.data


def test_health_route():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json == {"status": "ok"}


def test_unknown_route():
    client = app.test_client()
    response = client.get("/unknown")
    assert response.status_code == 404


def test_config_exists(monkeypatch):
    monkeypatch.setenv("APP_MODE", "testing")
    client = app.test_client()
    response = client.get("/config")
    assert response.status_code == 200
    assert response.get_json()["app_mode"] == "testing"


def test_config_missing(monkeypatch):
    monkeypatch.delenv("APP_MODE", raising=False)
    client = app.test_client()
    response = client.get("/config")
    assert response.status_code == 500


def test_grade_pass():
    client = app.test_client()
    response = client.post("/grade", json={"score": 80})
    assert response.status_code == 200
    assert response.get_json()["result"] == "pass"


def test_grade_fail():
    client = app.test_client()
    response = client.post("/grade", json={"score": 40})
    assert response.status_code == 200
    assert response.get_json()["result"] == "fail"


def test_grade_missing_score():
    client = app.test_client()
    response = client.post("/grade", json={})
    assert response.status_code == 400


def test_grade_invalid_type():
    client = app.test_client()
    response = client.post("/grade", json={"score": "high"})
    assert response.status_code == 400


def test_grade_out_of_range():
    client = app.test_client()
    response = client.post("/grade", json={"score": 120})
    assert response.status_code == 400
```

---

# Example ETL Tests

## `tests/test_etl.py`

```python
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
```

---

# How to Demonstrate Errors

A good CI/CD lesson should show both:

- success,
- and controlled failure.

When all tests pass, the pipeline is healthy.

To show the value of CI/CD, introduce a small intentional bug and rerun the tests.

---

## Error Scenario 1 — Break Homepage Text

In `app.py`, change:

```python
return "Student Portal CI/CD Demo"
```

to:

```python
return "Broken Home Page"
```

### Expected result
The homepage test fails because the output no longer matches the expected value.

### Teaching value
Shows application-level regression detection.

---

## Error Scenario 2 — Break Grading Logic

In `app.py`, change:

```python
result = "pass" if score >= 50 else "fail"
```

to:

```python
result = "pass" if score >= 90 else "fail"
```

### Expected result
The test for `score = 80` fails.

### Teaching value
Shows business-rule testing.

---

## Error Scenario 3 — Remove Duplicate Removal in ETL

In `etl.py`, comment out:

```python
df = df.drop_duplicates(subset=["student_id"])
```

### Expected result
The test checking duplicate IDs fails.

### Teaching value
Shows data-quality validation.

---

## Error Scenario 4 — Missing Required Column

Remove the `score` column in a test input or in ETL expectations.

### Expected result
The ETL test fails with:

```text
Missing required column: score
```

### Teaching value
Shows schema validation.

---

## Error Scenario 5 — Invalid Score Range

Put a value like `120` in the score field.

### Expected result
The score-range test fails.

### Teaching value
Shows business/data constraint validation.

---
