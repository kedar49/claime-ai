# Claime AI Backend

## Overview
This is the backend API for Claime AI, an AI-powered fact-checking system. It orchestrates agent workflows, generates PDF reports, and stores verdicts using decentralized storage.

## Features
- FastAPI-based REST API
- Multi-agent fact-checking pipeline
- PDF report generation
- Shelby Protocol integration for decentralized storage

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd claime-ai/backend
```

### 2. Python Environment
Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```
Or, if using Poetry:
```bash
poetry install
```

### 4. Environment Variables

**IMPORTANT**: Never commit secrets to version control!

Create a `.env` file in the `backend/` directory:

```bash
cp .env.example .env
```

Then edit `.env` with your actual API keys:

```env
# AI & LLM APIs
GOOGLE_API_KEY=your_actual_gemini_api_key
TAVILY_API_KEY=your_actual_tavily_api_key
```

**How to get these keys:**

- **GOOGLE_API_KEY**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)
- **TAVILY_API_KEY**: Sign up at [Tavily](https://tavily.com/)

⚠️ **Security Notes:**
- The `.env` file is already in `.gitignore` - never remove it from there
- Never hardcode keys in source code
- For CI/CD, use GitHub Secrets or similar secret management tools

### 5. Run the API Server
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### 6. Test the API
Visit [http://localhost:8000/docs](http://localhost:8000/docs) for interactive Swagger UI.

## Key Files
- `api.py` — Main FastAPI app
- `agents/` — Agent logic (FactChecker, ForensicExpert, TheJudge, Shelby)
- `storage/` — PDF reports and temporary files

## Useful Commands
- Run all tests:
  ```bash
  python -m unittest discover
  ```
- Format code:
  ```bash
  black .
  ```

## Troubleshooting
- Ensure all API keys are valid and set in `.env`
- For Shelby uploads, ensure the CLI is installed and configured

## License
MIT

---
For more details, see the main project [README](../README.md).
