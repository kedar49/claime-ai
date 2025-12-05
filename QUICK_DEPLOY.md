# ⚡ Quick Deploy to Vercel

**5-Minute Deployment Guide**

---

## 🚀 Step 1: Push to GitHub (2 min)

```bash
# Initialize git (if not done)
git init

# Add all files
git add .

# Commit
git commit -m "Ready for deployment"

# Create repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/claime-ai.git
git branch -M main
git push -u origin main
```

---

## 🔧 Step 2: Deploy Backend (2 min)

1. Go to: https://vercel.com/new
2. Import your GitHub repo
3. **Settings**:
   - Name: `claime-ai-backend`
   - Root Directory: `backend`
4. **Environment Variables**:
   ```
   GOOGLE_API_KEY = your_key_here
   TAVILY_API_KEY = your_key_here
   ```
5. Click **Deploy**
6. **Copy your backend URL**: `https://claime-ai-backend.vercel.app`

---

## 🎨 Step 3: Deploy Frontend (1 min)

1. Go to: https://vercel.com/new
2. Import the SAME GitHub repo
3. **Settings**:
   - Name: `claime-ai`
   - Root Directory: `frontend`
4. **Environment Variables**:
   ```
   NEXT_PUBLIC_API_BASE_URL = https://claime-ai-backend.vercel.app
   ```
   (Use YOUR backend URL from Step 2!)
5. Click **Deploy**

---

## ✅ Done!

Your app is live at: `https://claime-ai.vercel.app`

Test it:
1. Visit your URL
2. Enter a claim
3. Click "Verify Claim"
4. See results! 🎉

---

## 🆘 Issues?

See detailed guide: `VERCEL_DEPLOYMENT_GUIDE.md`

---

**That's it! Your project is deployed! 🚀**
