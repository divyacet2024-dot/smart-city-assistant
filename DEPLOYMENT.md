# Deployment Instructions for Smart Bin

## Option 1: Deploy to Render.com (Free)

### Step 1: Push to GitHub
Your project is already on GitHub ✓

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up with your GitHub account

### Step 3: Create Web Service
1. In Render dashboard, click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: smart-bin
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
4. Click "Create Web Service"

### Step 4: Add Environment Variables
In Render dashboard, go to "Environment" and add:
- Key: `GEMINI_API_KEY`
- Value: (your Gemini API key)

### Step 5: Your URL
Once deployed, Render will give you a URL like:
`https://smart-bin.onrender.com`

---

## Option 2: Deploy to Railway

### Step 1: Go to Railway
1. Visit https://railway.app
2. Sign up with GitHub

### Step 2: Deploy
1. Click "New Project" → "Deploy from GitHub repo"
2. Select your repository
3. Add environment variable `GEMINI_API_KEY`
4. Click "Deploy"

### Step 3: Get URL
Your app URL will be provided after deployment

---

## Option 3: Deploy to Replit (Easiest)

### Step 1: Import
1. Go to https://replit.com
2. Click "Import from GitHub"
3. Select your repository

### Step 2: Configure
- Language: Python
- Run command: `python app.py`

### Step 3: Add Secrets
In Replit "Secrets" tab, add:
- Key: `GEMINI_API_KEY`
- Value: (your API key)

### Step 4: Deploy
Click "Deploy" button

---

## Important: Update app.py for Production

Before deploying, update your app.py to use the correct port:

```python
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
```

---

## Get Free Gemini API Key
1. Go to https://aistudio.google.com/app/apikey
2. Create new API key
3. Add to your deployment environment variables

---

## Demo Link Format
Once deployed, your demo link will be:
- Render: `https://your-app-name.onrender.com`
- Railway: `https://your-app-name.up.railway.app`
- Replit: `https://your-app-name.replit.app`
