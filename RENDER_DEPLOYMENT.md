# Render.com Free Deployment - Step by Step

## What You Get (Free):
- ✓ Unlimited apps
- ✓ 750 compute hours/month (enough for always-on hobby project)
- ✓ Free PostgreSQL database (if needed later)
- ✓ Free SSL/HTTPS
- ✓ Automatic deploys from GitHub
- ✓ Custom domain support
- ✓ No credit card required (option available)

---

## Step 1: Create GitHub Account & Push Code

### 1.1 Install Git (if not installed):
Download from https://git-scm.com/download/win

### 1.2 Create GitHub Account:
Go to https://github.com/signup (free)

### 1.3 Create New Repository on GitHub:
- Click "+" → "New repository"
- Name: `projectk`
- Description: "PC Builder with Authentication"
- Select "Public" (for free)
- Click "Create repository"

### 1.4 Push Your Code to GitHub:
Open PowerShell in your project folder:
```powershell
cd c:\Users\LEENOVO\Desktop\projectk

git config --global user.email "your-email@example.com"
git config --global user.name "Your Name"

git init
git add .
git commit -m "Initial commit - PC Builder with Auth"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/projectk.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your actual GitHub username.

---

## Step 2: Prepare Your Project for Render

Files already created:
- ✓ `Procfile` - tells Render how to start your app
- ✓ `runtime.txt` - specifies Python version
- ✓ `requirements.txt` - all dependencies

Verify `requirements.txt` has gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

Push this update:
```powershell
git add requirements.txt
git commit -m "Add gunicorn"
git push origin main
```

---

## Step 3: Deploy on Render (The Easy Part!)

### 3.1 Sign Up on Render:
Go to https://render.com/register
- Click "Sign up with GitHub" (easier)
- Authorize connection
- Done!

### 3.2 Create New Web Service:
- Click "New +" button
- Select "Web Service"
- Click "Connect" next to your `projectk` repository
- If it's not showing, click "+ Connect account" and authenticate

### 3.3 Configure Deployment:
Fill in these fields:

| Field | Value |
|-------|-------|
| **Name** | pc-builder |
| **Environment** | Python 3 |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn run:app` |

### 3.4 Scroll Down - Select Free Plan:
- **Instance Type**: Free
- **Auto-deploy**: ON (auto-deploys on git push)

### 3.5 Click "Create Web Service"
Wait 2-3 minutes... 🚀

---

## Step 4: Get Your Live URL

Once deployed (green checkmark appears):
- Your app is live at: `https://pc-builder.onrender.com`
- Share this URL with anyone!

---

## What Happens Next:

✓ Your app runs 24/7 (free tier never sleeps)
✓ Every time you push to GitHub, Render auto-deploys
✓ Database persists (SQLite works fine, data saved)
✓ HTTPS enabled automatically
✓ No credit card needed (free forever)

---

## Make Updates & Deploy:

After any changes:
```powershell
git add .
git commit -m "Your message"
git push origin main
```

Render auto-deploys in 1-2 minutes. Watch the logs in Render dashboard.

---

## Quick Checklist:

- [ ] Create GitHub account
- [ ] Create `projectk` repository
- [ ] Push code to GitHub
- [ ] Sign up on Render.com with GitHub
- [ ] Create Web Service
- [ ] Set free plan
- [ ] Wait for deployment
- [ ] Get your live URL

---

## If Deployment Fails:

Check the Render logs:
1. Go to your service on Render
2. Click "Logs" tab
3. Look for errors
4. Common fixes:
   - Missing dependency in `requirements.txt`
   - Wrong start command
   - Port binding issue

---

## Free Forever Plan Details:

**Included:**
- 750 compute hours/month (~1000 minutes/day)
- Enough for: personal use, demos, low-traffic sites
- Data persistence: YES
- HTTPS: YES
- Downtime: NO
- Bandwidth: Unlimited

**Not included:**
- Email support (community only)
- Advanced analytics

---

## Total Time to Live:
⏱️ **~15 minutes** from now to having your PC Builder live on the internet!

---

## Your Live App Will Have:
✓ Login page: `https://pc-builder.onrender.com/login`
✓ Signup page: `https://pc-builder.onrender.com/signup`
✓ API endpoints for authentication
✓ All existing features
✓ Persistent database
✓ Free SSL/HTTPS
✓ Auto-updates on git push

Let me know when you've completed each step!
