# 🚨 Backend Deployment Issue - SOLUTION

## The Problem

Your backend is crashing on Vercel because:

1. **Too Heavy for Serverless**: Your AI agents with LangChain, LangGraph, and Gemini are too resource-intensive
2. **Cold Start Timeout**: Vercel serverless functions timeout during initialization
3. **Memory Limits**: AI models and dependencies exceed Vercel's 1GB memory limit
4. **Package Size**: Your dependencies are too large for Vercel's 50MB limit

## ✅ RECOMMENDED SOLUTION: Split Deployment

### Deploy Frontend on Vercel ✅
### Deploy Backend on Railway/Render 🚂

---

## 🚀 Option 1: Railway (Recommended)

Railway is perfect for Python backends with AI workloads.

### Step 1: Deploy Backend to Railway

1. **Go to Railway**: https://railway.app/
2. **Sign up** with GitHub
3. **New Project** → **Deploy from GitHub repo**
4. **Select your repository**
5. **Configure**:
   - Root Directory: `backend`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

6. **Add Environment Variables**:
   ```
   GOOGLE_API_KEY=your_key
   TAVILY_API_KEY=your_key
   PORT=8000
   ```

7. **Deploy** - Railway will give you a URL like: `https://your-app.railway.app`

### Step 2: Update Frontend to Use Railway Backend

Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=https://your-app.railway.app
```

### Step 3: Deploy Frontend to Vercel

```bash
cd frontend
vercel --prod
```

---

## 🚀 Option 2: Render

### Step 1: Deploy Backend to Render

1. **Go to Render**: https://render.com/
2. **Sign up** with GitHub
3. **New** → **Web Service**
4. **Connect your repository**
5. **Configure**:
   - Name: `claime-ai-backend`
   - Root Directory: `backend`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api:app --host 0.0.0.0 --port $PORT`

6. **Add Environment Variables**:
   ```
   GOOGLE_API_KEY=your_key
   TAVILY_API_KEY=your_key
   ```

7. **Create Web Service** - You'll get a URL like: `https://claime-ai-backend.onrender.com`

### Step 2: Update Frontend

Edit `frontend/.env.local`:
```env
NEXT_PUBLIC_API_BASE_URL=https://claime-ai-backend.onrender.com
```

### Step 3: Deploy Frontend to Vercel

```bash
cd frontend
vercel --prod
```

---

## 🚀 Option 3: Keep Both on Vercel (NOT RECOMMENDED)

If you must use Vercel for backend, you need to:

### 1. Create Lightweight API Wrapper

Create `backend/api_vercel.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "online", "service": "Claime AI API"}

@app.post("/verify")
async def verify_claim_simple(request: dict):
    # This won't work well - too heavy for serverless
    return {"error": "Use Railway or Render for full functionality"}
```

### 2. Update vercel.json

```json
{
    "version": 2,
    "builds": [
        {
            "src": "backend/api_vercel.py",
            "use": "@vercel/python",
            "config": {
                "maxLambdaSize": "50mb"
            }
        }
    ]
}
```

**⚠️ This will NOT work well for AI workloads!**

---

## 📋 Comparison

| Platform | Backend | Frontend | Cost | AI Support |
|----------|---------|----------|------|------------|
| **Railway** | ✅ Excellent | ❌ No | $5/mo | ✅ Perfect |
| **Render** | ✅ Good | ❌ No | Free tier | ✅ Good |
| **Vercel** | ❌ Poor | ✅ Excellent | Free | ❌ Bad |
| **Heroku** | ✅ Good | ❌ No | $7/mo | ✅ Good |

---

## 🎯 RECOMMENDED SETUP

```
Frontend (Vercel)          Backend (Railway)
    ↓                           ↓
https://claime-ai.vercel.app → https://api.railway.app
```

### Benefits:
- ✅ Frontend: Fast CDN delivery
- ✅ Backend: No cold starts
- ✅ Backend: Unlimited execution time
- ✅ Backend: More memory for AI
- ✅ Backend: Better for long-running tasks

---

## 🚀 Quick Start: Railway Deployment

### 1. Create `railway.json` in backend folder:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn api:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### 2. Create `Procfile` in backend folder:

```
web: uvicorn api:app --host 0.0.0.0 --port $PORT
```

### 3. Deploy:

1. Push to GitHub
2. Go to Railway.app
3. New Project → Deploy from GitHub
4. Select repository
5. Add environment variables
6. Deploy!

---

## 🔧 Update Frontend After Backend Deployment

### 1. Get your Railway URL
Example: `https://claime-ai-backend-production.up.railway.app`

### 2. Update frontend/.env.local:
```env
NEXT_PUBLIC_API_BASE_URL=https://claime-ai-backend-production.up.railway.app
```

### 3. Redeploy frontend:
```bash
cd frontend
vercel --prod
```

---

## ✅ Final Architecture

```
User Browser
     ↓
Vercel CDN (Frontend)
     ↓
Railway (Backend API)
     ↓
Google Gemini AI
Tavily Search API
```

---

## 📝 Summary

**Current Issue:** Vercel can't handle heavy AI backend

**Solution:** 
1. Deploy backend to Railway/Render
2. Keep frontend on Vercel
3. Update frontend to point to new backend URL

**Next Steps:**
1. Choose Railway or Render
2. Deploy backend there
3. Get backend URL
4. Update frontend environment variable
5. Redeploy frontend

---

**Railway is the best choice for your AI backend!** 🚂
