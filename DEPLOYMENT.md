# Deployment Guide - Token Economics Calculator

This guide explains how to deploy the web version of the Token Economics Calculator online.

## Web Version (app.py)

The web version is built with **Streamlit** and can be easily deployed for free.

### Option 1: Streamlit Community Cloud (Recommended - FREE)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO_URL
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository, branch (main), and main file path (`app.py`)
   - Click "Deploy"
   - Your app will be live at: `https://YOUR-APP-NAME.streamlit.app`

**That's it!** Streamlit Cloud handles everything automatically.

### Option 2: Run Locally for Testing

```bash
# Install streamlit
pip install streamlit

# Run the web app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Option 3: Other Hosting Platforms

#### Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT
   ```
2. Deploy via Heroku CLI or GitHub integration

#### Railway.app
1. Connect your GitHub repo
2. Railway auto-detects Streamlit apps
3. Deploy with one click

#### Render.com
1. Connect your GitHub repo
2. Set build command: `pip install -r requirements.txt`
3. Set start command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0`

## Desktop Version (run.py)

The desktop version uses tkinter and runs locally:

```bash
python run.py
```

Cannot be deployed as a web app (requires desktop GUI).

## Files Overview

- `app.py` - Web version (Streamlit)
- `run.py` - Desktop version (tkinter)
- `requirements.txt` - Python dependencies
- `README.md` - General documentation
- `DEPLOYMENT.md` - This file

## Environment Variables

No environment variables needed for basic deployment.

## Cost

- **Streamlit Community Cloud**: FREE (unlimited public apps)
- **Heroku**: FREE tier available (with limitations)
- **Railway.app**: FREE tier available ($5 credit/month)
- **Render.com**: FREE tier available

## Post-Deployment

After deploying, you can:
1. Share the URL with anyone
2. Customize the domain (on paid plans)
3. Add analytics
4. Enable authentication (if needed)

## Support

For deployment issues:
- Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)
- Community forum: [discuss.streamlit.io](https://discuss.streamlit.io)

