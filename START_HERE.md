# 🚀 START HERE - MoveH Quick Start

## ✅ Setup Complete!

All blockchain functionality has been removed. The project is now ready to run as a pure AI fact-checking system.

## 📋 Prerequisites Check

- ✅ Python 3.12+ installed
- ✅ Dependencies installed (`pip install -r requirements.txt`)
- ⚠️ **API Keys Required** - See step 1 below

## 🔑 Step 1: Configure API Keys

Edit `backend/.env` and add your API keys:

```env
GOOGLE_API_KEY=your_actual_gemini_api_key_here
TAVILY_API_KEY=your_actual_tavily_api_key_here
```

**Get your keys:**
- **Google Gemini**: https://aistudio.google.com/app/apikey (Free tier available)
- **Tavily**: https://tavily.com/ (Free tier: 1000 requests/month)

## 🚀 Step 2: Start the Backend

### Option A: Using the batch file (Windows)
```bash
cd backend
start.bat
```

### Option B: Using uvicorn directly
```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Option C: Using Python directly
```bash
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

The server will start at: **http://localhost:8000**

## 🧪 Step 3: Test the API

### Open Swagger UI
Visit: http://localhost:8000/docs

### Test with curl
```bash
curl -X POST "http://localhost:8000/verify" ^
  -H "Content-Type: application/json" ^
  -d "{\"claim\": \"Tesla announced they are acquiring Twitter for $100 billion\"}"
```

### Test with the CLI
```bash
cd backend
python main.py
```

## 📊 What You Can Do

### 1. **API Endpoints**
- `POST /verify` - Verify a claim (non-streaming)
- `POST /verify_stream` - Verify with real-time updates (SSE)
- `GET /` - Health check

### 2. **CLI Mode**
Interactive terminal interface:
```bash
python main.py
```

### 3. **Frontend** (Optional)
```bash
cd frontend
pnpm install
pnpm dev
```
Visit: http://localhost:3000

## 🎯 Quick Test Examples

Try these claims:

1. **True Claim**: "Apple Inc. reported Q4 2025 earnings of $1.95 per share"
2. **False Claim**: "Tesla is acquiring Twitter for $100 billion"
3. **Suspicious Claim**: "URGENT!!! Amazon is bankrupt! CLICK HERE NOW!"

## 📁 Project Structure

```
moveh/
├── backend/
│   ├── agents/          # AI agents (Fact Checker, Forensic Expert, Judge)
│   ├── storage/         # PDF reports
│   ├── api.py          # FastAPI server
│   ├── main.py         # CLI interface
│   ├── .env            # Your API keys (NEVER commit!)
│   └── requirements.txt
├── frontend/           # Next.js UI (optional)
└── README.md
```

## ⚠️ Troubleshooting

### "Module not found" errors
```bash
cd backend
pip install -r requirements.txt
```

### "API key not found" errors
Make sure your `.env` file has valid keys without quotes:
```env
GOOGLE_API_KEY=AIzaSyD...
TAVILY_API_KEY=tvly-...
```

### Port 8000 already in use
```bash
uvicorn api:app --reload --port 8001
```

### Import errors
Make sure you're in the `backend` directory when running commands.

## 📚 Documentation

- **Backend README**: `backend/README.md`
- **Quick Start**: `backend/QUICKSTART.md`
- **Removal Summary**: `BLOCKCHAIN_REMOVAL_SUMMARY.md`
- **Main README**: `README.md`

## 🎉 You're Ready!

The project is fully functional without blockchain. All AI agents work perfectly:
- ✅ Fact Checker (web search & evidence)
- ✅ Forensic Expert (linguistic analysis)
- ✅ The Judge (final verdict)
- ✅ PDF report generation
- ✅ Shelby storage (optional)

**Next Steps:**
1. Add your API keys to `backend/.env`
2. Run `cd backend && start.bat` (or use uvicorn)
3. Visit http://localhost:8000/docs
4. Start fact-checking!

---

**Need Help?** Check the documentation files or run `python test_full_system.py` to verify everything works.
