# 🚀 Quick Start Guide

## Prerequisites
- Python 3.12 or higher
- pip (Python package manager)

## Installation Steps

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure API Keys
Edit the `.env` file and add your API keys:
```env
GOOGLE_API_KEY=your_actual_gemini_api_key
TAVILY_API_KEY=your_actual_tavily_api_key
```

**Get your API keys:**
- **Google Gemini**: https://aistudio.google.com/app/apikey
- **Tavily**: https://tavily.com/

### 3. Run the API Server
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: http://localhost:8000

### 4. Test the API
Open your browser and visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 5. Run CLI Mode (Optional)
```bash
python main.py
```

## Quick Test

Test with a sample claim:
```bash
curl -X POST "http://localhost:8000/verify" \
  -H "Content-Type: application/json" \
  -d '{"claim": "Tesla announced they are acquiring Twitter for $100 billion"}'
```

## Troubleshooting

### Import Errors
If you get import errors, make sure you're in the backend directory:
```bash
cd backend
pip install -r requirements.txt
```

### API Key Errors
Make sure your `.env` file has valid API keys without quotes:
```env
GOOGLE_API_KEY=AIzaSyD...
TAVILY_API_KEY=tvly-...
```

### Port Already in Use
If port 8000 is busy, use a different port:
```bash
uvicorn api:app --reload --port 8001
```

## What's Next?

- Check out the [README.md](README.md) for detailed documentation
- Explore the API at http://localhost:8000/docs
- Try the CLI with `python main.py`
- Run tests with `python test_full_system.py`
