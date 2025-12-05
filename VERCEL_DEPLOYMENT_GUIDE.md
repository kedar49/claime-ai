# 🚀 Vercel Deployment Guide for Claime AI

Complete guide to deploy both frontend and backend to Vercel.

---

## 📋 Prerequisites

1. ✅ **Vercel Account** - Sign up at https://vercel.com
2. ✅ **GitHub Account** - Your code should be in a GitHub repository
3. ✅ **API Keys Ready**:
   - Google Gemini API Key
   - Tavily API Key

---

## 🎯 Deployment Strategy

We'll deploy in two parts:
1. **Backend** (FastAPI) → Separate Vercel project
2. **Frontend** (Next.js) → Separate Vercel project

---

## Part 1: Deploy Backend 🔧

### Step 1: Prepare Backend for Deployment

The following files have been created for you:
- ✅ `backend/vercel.json` - Vercel configuration
- ✅ `backend/requirements-vercel.txt` - Optimized dependencies
- ✅ `backend/api_vercel.py` - Serverless wrapper
- ✅ `.vercelignore` - Files to exclude

### Step 2: Push to GitHub

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "Prepare for Vercel deployment"

# Create GitHub repository and push
git remote add origin https://github.com/kedar49/claime-ai.git
git branch -M main
git push -u origin main
```

### Step 3: Deploy Backend to Vercel

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard

2. **Click "Add New Project"**

3. **Import your GitHub repository**

4. **Configure Project**:
   - **Project Name**: `claime-ai-backend`
   - **Framework Preset**: Other
   - **Root Directory**: `backend`
   - **Build Command**: Leave empty
   - **Output Directory**: Leave empty

5. **Add Environment Variables**:
   Click "Environment Variables" and add:
   
   ```
   GOOGLE_API_KEY = your_google_api_key_here
   TAVILY_API_KEY = your_tavily_api_key_here
   BACKEND_URL = https://claime-ai-backend.vercel.app
   ```

6. **Click "Deploy"**

7. **Wait for deployment** (2-3 minutes)

8. **Copy your backend URL**: 
   - Example: `https://claime-ai-backend.vercel.app`
   - Save this for frontend configuration!

### Step 4: Test Backend Deployment

Visit your backend URL:
```
https://claime-ai-backend.vercel.app/
```

You should see:
```json
{"status":"online","service":"Claime API"}
```

Test API docs:
```
https://claime-ai-backend.vercel.app/docs
```

---

## Part 2: Deploy Frontend 🎨

### Step 1: Update Frontend Environment

Edit `frontend/.env.production`:
```env
NEXT_PUBLIC_API_BASE_URL=https://claime-ai-backend.vercel.app
```

**Important**: Replace with your actual backend URL from Part 1!

### Step 2: Commit Changes

```bash
git add frontend/.env.production
git commit -m "Update production API URL"
git push
```

### Step 3: Deploy Frontend to Vercel

1. **Go to Vercel Dashboard**: https://vercel.com/dashboard

2. **Click "Add New Project"**

3. **Import the SAME GitHub repository**

4. **Configure Project**:
   - **Project Name**: `claime-ai`
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `pnpm build` (or `npm run build`)
   - **Output Directory**: `.next`

5. **Environment Variables**:
   Add this variable:
   ```
   NEXT_PUBLIC_API_BASE_URL = https://claime-ai-backend.vercel.app
   ```
   (Use your actual backend URL!)

6. **Click "Deploy"**

7. **Wait for deployment** (3-5 minutes)

8. **Your app is live!** 🎉
   - Example: `https://claime-ai.vercel.app`

---

## 🧪 Testing Your Deployment

### Test Backend
```bash
# Health check
curl https://claime-ai-backend.vercel.app/

# Test verification endpoint
curl -X POST "https://claime-ai-backend.vercel.app/verify" \
  -H "Content-Type: application/json" \
  -d '{"claim": "Tesla is acquiring Twitter"}'
```

### Test Frontend
1. Visit: `https://claime-ai.vercel.app`
2. Enter a claim: "Apple reported Q4 earnings"
3. Click "Verify Claim"
4. Should see results! ✅

---

## ⚙️ Configuration Files Created

### Backend Files:
```
backend/
├── vercel.json              ✅ Vercel config
├── requirements-vercel.txt  ✅ Optimized dependencies
└── api_vercel.py           ✅ Serverless wrapper
```

### Frontend Files:
```
frontend/
└── .env.production         ✅ Production environment
```

### Root Files:
```
.vercelignore              ✅ Deployment exclusions
```

---

## 🔧 Troubleshooting

### Backend Issues

#### Error: "Module not found"
**Solution**: Check `backend/requirements-vercel.txt` includes all dependencies

#### Error: "Function timeout"
**Solution**: Vercel free tier has 10s timeout. Optimize your code or upgrade plan.

#### Error: "Environment variable not found"
**Solution**: 
1. Go to Vercel Dashboard → Your Backend Project → Settings → Environment Variables
2. Add missing variables
3. Redeploy

### Frontend Issues

#### Error: "Failed to fetch"
**Solution**: 
1. Check `NEXT_PUBLIC_API_BASE_URL` is correct
2. Make sure backend is deployed and working
3. Check browser console for CORS errors

#### Error: "API endpoint not found"
**Solution**: Verify backend URL in `.env.production` matches your actual backend deployment

---

## 🔄 Updating Your Deployment

### Update Backend:
```bash
# Make changes to backend code
git add backend/
git commit -m "Update backend"
git push
```
Vercel will auto-deploy!

### Update Frontend:
```bash
# Make changes to frontend code
git add frontend/
git commit -m "Update frontend"
git push
```
Vercel will auto-deploy!

---

## 📊 Monitoring

### View Logs:
1. Go to Vercel Dashboard
2. Select your project
3. Click "Deployments"
4. Click on a deployment
5. View "Functions" tab for backend logs

### Check Performance:
- Vercel Dashboard → Analytics
- Monitor response times
- Check error rates

---

## 💰 Pricing Considerations

### Vercel Free Tier Includes:
- ✅ Unlimited deployments
- ✅ 100GB bandwidth/month
- ✅ Serverless function execution
- ✅ Automatic HTTPS
- ✅ Custom domains

### Limitations:
- ⚠️ 10s function timeout (backend)
- ⚠️ 100GB bandwidth limit
- ⚠️ 6000 build minutes/month

**For production**: Consider upgrading to Pro ($20/month) for:
- 60s function timeout
- 1TB bandwidth
- Better performance

---

## 🌐 Custom Domain (Optional)

### Add Custom Domain:

1. **Go to Project Settings** → Domains

2. **Add your domain**: `claime-ai.com`

3. **Configure DNS**:
   - Add CNAME record pointing to `cname.vercel-dns.com`
   - Or use Vercel nameservers

4. **Wait for DNS propagation** (5-30 minutes)

5. **Your app is live on custom domain!** 🎉

---

## 🔒 Security Best Practices

### Environment Variables:
- ✅ Never commit `.env` files
- ✅ Use Vercel's environment variables
- ✅ Rotate API keys regularly

### API Keys:
- ✅ Keep them secret
- ✅ Use different keys for dev/prod
- ✅ Monitor usage

### CORS:
- ✅ Configure allowed origins in backend
- ✅ Don't use `allow_origins=["*"]` in production

---

## 📝 Deployment Checklist

### Before Deployment:
- [ ] Code pushed to GitHub
- [ ] API keys ready
- [ ] `.env.production` configured
- [ ] All dependencies in `requirements-vercel.txt`

### Backend Deployment:
- [ ] Backend deployed to Vercel
- [ ] Environment variables added
- [ ] Health check working (`/` endpoint)
- [ ] API docs accessible (`/docs`)
- [ ] Backend URL copied

### Frontend Deployment:
- [ ] Backend URL added to frontend env
- [ ] Frontend deployed to Vercel
- [ ] Can access homepage
- [ ] Can verify claims
- [ ] PDF download works

### Post-Deployment:
- [ ] Test full verification flow
- [ ] Check logs for errors
- [ ] Monitor performance
- [ ] Share with users! 🎉

---

## 🆘 Need Help?

### Vercel Documentation:
- https://vercel.com/docs
- https://vercel.com/docs/frameworks/nextjs
- https://vercel.com/docs/functions/serverless-functions/runtimes/python

### Common Issues:
- Check Vercel deployment logs
- Verify environment variables
- Test backend independently
- Check browser console

---

## 🎉 Success!

Your Claime AI application is now deployed and accessible worldwide!

**Backend**: `https://claime-ai-backend.vercel.app`  
**Frontend**: `https://claime-ai.vercel.app`

Share it with:
- Prof. Gopal Deshmukh Sir
- Your classmates
- The world! 🌍

---

**Built with ❤️ by Kedar Sathe & Riddhi Shende**

**7th Semester Major Project**  
**Under the guidance of Prof. Gopal Deshmukh Sir**
