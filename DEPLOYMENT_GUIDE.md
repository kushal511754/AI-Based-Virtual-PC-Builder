# Free Deployment Guide for PC Builder

## Option 1: Heroku (Easiest, Recommended for Flask)
**Cost**: Free tier available (with limitations)
**Setup Time**: 10-15 minutes

### Steps:
1. Sign up at https://www.heroku.com
2. Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
3. In your project directory, create `Procfile`:
```
web: gunicorn run:app
```

4. Create `runtime.txt`:
```
python-3.10.12
```

5. Update `requirements.txt` to include gunicorn:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

6. Modify `run.py` to work with Gunicorn:
```python
from server.app import create_app

app = create_app()

if __name__ == '__main__':
    app.run()
```

7. Deploy:
```bash
heroku login
heroku create your-app-name
git push heroku main
```

**Pros**: Simple deployment, Flask-native, automatic HTTPS
**Cons**: Free tier has limitations (500MB disk, sleeps after 30 mins inactivity)

---

## Option 2: Render.com (Free + Good Performance)
**Cost**: Free tier available
**Setup Time**: 15-20 minutes

### Steps:
1. Sign up at https://render.com
2. Create `Procfile` (same as Heroku)
3. Push code to GitHub
4. In Render dashboard:
   - Click "New +" → "Web Service"
   - Connect your GitHub repo
   - Set start command: `gunicorn run:app`
   - Environment: Python 3.10
   - Deploy

**Pros**: Free tier is more generous, better performance, 750 free hours/month
**Cons**: Spins down after inactivity (similar to Heroku)

---

## Option 3: PythonAnywhere (Python-Specific)
**Cost**: Free tier available
**Setup Time**: 20-25 minutes

### Steps:
1. Sign up at https://www.pythonanywhere.com
2. Upload your project via Git or ZIP
3. Set up Virtual Environment
4. Create Web App with Flask
5. Configure WSGI file:
```python
import sys
path = '/home/yourusername/projectk'
sys.path.append(path)

from server.app import create_app
app = create_app()
```

6. Point domain and enable HTTPS

**Pros**: Python-specific, good free tier, easy UI
**Cons**: Limited to subdomain URL, storage limits

---

## Option 4: Replit (For Testing/Development)
**Cost**: Free tier available
**Setup Time**: 5 minutes

### Steps:
1. Go to https://replit.com
2. Create new Replit, select Python
3. Upload your project
4. Create `.replit` file:
```
run = "python run.py"
```

5. Click "Run"

**Pros**: Instant deployment, no configuration needed, live URL
**Cons**: Goes to sleep, not recommended for production

---

## Option 5: Railway (Modern Alternative)
**Cost**: Free trial with $5 credit
**Setup Time**: 10-15 minutes

### Steps:
1. Sign up at https://railway.app
2. Connect GitHub repo
3. Railway auto-detects Python project
4. Deploy automatically

**Pros**: Modern UI, easy deployment, good free tier
**Cons**: Free tier eventually expires

---

## Database Configuration for Deployment

### Important: Use PostgreSQL instead of SQLite for production

Update `server/utils/db.py`:
```python
import os
import psycopg2
from contextlib import contextmanager

DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///database.db')

@contextmanager
def get_db():
    if DATABASE_URL.startswith('postgres'):
        # Use PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
    else:
        # Use SQLite for development
        conn = sqlite3.connect(DATABASE_PATH)
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()
```

---

## Step-by-Step: Deploy to Render (Recommended)

### 1. Prepare Your Code
```bash
cd c:\Users\LEENOVO\Desktop\projectk
pip install gunicorn
pip freeze > requirements.txt
```

### 2. Create Deployment Files

**Procfile** (in project root):
```
web: gunicorn run:app
```

**runtime.txt** (in project root):
```
python-3.10.12
```

### 3. Update run.py
```python
"""Flask application entry point."""
import os
import sys
import logging

# Add project root to path
sys.path.insert(0, os.path.dirname(__file__))

from server.app import create_app

# Create app
app = create_app()

if __name__ == '__main__':
    # Development
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
```

### 4. Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/yourusername/projectk.git
git push -u origin main
```

### 5. Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub account
4. Select your repository
5. Fill in:
   - **Name**: pc-builder
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn run:app`
6. Click "Deploy"

**Your site will be live at**: `https://pc-builder.onrender.com`

---

## Environment Variables for Production

Create `.env` file (don't commit to Git):
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host/dbname
SECRET_KEY=your-secret-key-here
```

Update `server/app.py`:
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-key')
```

---

## Domain Configuration

### Free Domain Options:
1. **Freenom** - https://www.freenom.com (free .tk, .ml, .ga)
2. **Render's Free Domain** - auto-assigned subdomain
3. **GitHub Pages** (static sites only)

### Point Custom Domain to Render:
1. Get your Render domain (e.g., pc-builder.onrender.com)
2. Go to domain registrar DNS settings
3. Add CNAME record pointing to Render

---

## Quick Comparison

| Platform | Free Tier | Setup | Performance | Cold Start |
|----------|-----------|-------|-------------|-----------|
| Heroku | Limited | Easy | Good | 30s |
| Render | Generous | Easy | Great | 30s |
| PythonAnywhere | Limited | Medium | Good | None |
| Railway | $5 credit | Easy | Great | 5s |
| Replit | Yes | Fastest | Fair | None |

---

## Next Steps

1. **Choose a platform** (Render recommended)
2. **Create GitHub account** if you don't have one
3. **Push your code** to GitHub
4. **Connect platform** to your GitHub repo
5. **Set environment variables** on the platform
6. **Deploy** with one click
7. **Get your live URL** and share!

---

## Troubleshooting

### App won't start
- Check `requirements.txt` has all dependencies
- Ensure `Procfile` is in project root
- Review deployment logs on platform

### Database errors
- Use PostgreSQL for production, not SQLite
- Set `DATABASE_URL` environment variable
- Run migrations if needed

### Cold start delays
- Normal for free tiers
- Consider Railway or paid tiers for always-on

### CORS/SSL errors
- Platform handles SSL automatically
- Add domain to Flask's allowed hosts if needed

---

## Cost Estimate for Scaling

| Traffic | Solution | Cost |
|---------|----------|------|
| <1,000 users/month | Free tier | $0 |
| 1,000-10,000 users | Render/Railway | $5-10/month |
| 10,000+ users | Heroku Pro / Railway | $25-50/month |

**Start free, scale as needed!**
