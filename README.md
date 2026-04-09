# GitHub Actions CI/CD Demo

A minimal Flask app for demonstrating a CI pipeline with GitHub Actions.

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

The workflow is in `.github/workflows/ci.yml` and will:
- run on push to `main`
- install dependencies
- run tests
- package the app as a zip
- upload the zip as an artifact
