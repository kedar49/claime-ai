# 🔧 PDF Download Fix

## The Issue
The PDF download was failing because the URL was relative (`/download/filename.pdf`) instead of absolute.

## ✅ What Was Fixed

1. **Updated `backend/agents/shelby.py`**:
   - Changed local URL from `/download/{filename}` to `http://localhost:8000/download/{filename}`
   - Now uses `BACKEND_URL` environment variable (defaults to `http://localhost:8000`)

2. **The `/download` route is properly mounted** in `backend/api.py`:
   ```python
   app.mount("/download", StaticFiles(directory=STORAGE_DIR), name="download")
   ```

## 🧪 Test the Fix

### Option 1: Test in Browser
1. Make sure backend is running
2. Visit: http://localhost:8000/download/moveh_report_20251205_170327.pdf
3. PDF should download automatically

### Option 2: Test with curl
```bash
curl -I http://localhost:8000/download/moveh_report_20251205_170327.pdf
```

Should return:
```
HTTP/1.1 200 OK
content-type: application/pdf
```

### Option 3: Test Full Flow
1. Go to frontend: http://localhost:3000
2. Enter a claim: "Tesla is acquiring Twitter"
3. Click "Verify Claim"
4. Wait for results
5. Click "Download AEP Report"
6. PDF should download! ✅

## 🔄 Restart Required

**You need to restart the backend** for the changes to take effect:

```bash
# In backend terminal, press Ctrl+C
# Then restart:
cd backend
python -m uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

## 📁 Existing PDFs

You have these PDFs already generated:
- `moveh_report_20251130_125712.pdf`
- `moveh_report_20251130_130655.pdf`
- `moveh_report_20251205_170228.pdf`
- `moveh_report_20251205_170327.pdf`

Test with any of them:
```
http://localhost:8000/download/moveh_report_20251205_170327.pdf
```

## ⚙️ Optional: Custom Backend URL

If your backend runs on a different port or domain, set it in `backend/.env`:

```env
BACKEND_URL=http://localhost:8001
```

Or for production:
```env
BACKEND_URL=https://your-domain.com
```

## 🎯 Summary

**Before:** `/download/filename.pdf` (relative URL - doesn't work from frontend)
**After:** `http://localhost:8000/download/filename.pdf` (absolute URL - works!)

**Restart the backend and try downloading a PDF again!** 🚀
