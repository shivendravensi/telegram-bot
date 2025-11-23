# 🚀 Render Deployment Guide
## Telegram File Transfer Bot

### Step 1: Prepare Your Local Setup

#### A. Get OAuth Credentials (Local First)
```bash
# Copy your existing bot files
cp bot_master.py generate_token.py ./
cp oauth_credentials.json ./

# Generate token.json locally
python generate_token.py
```

This will create `token.json` which you'll upload to Render.

#### B. Test Locally First
```bash
# Set environment variable
set BOT_TOKEN=your_bot_token_here

# Test locally
python bot_render.py
```

### Step 2: Create GitHub Repository

```bash
# Initialize git
git init

# Add files
git add .

# Commit
git commit -m "Telegram to Google Drive Bot - Render Deployment"

# Create GitHub repository and push
git remote add origin https://github.com/yourusername/telegram-bot.git
git push -u origin main
```

### Step 3: Deploy to Render

#### A. Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Connect your repository

#### B. Create Web Service
1. Click "New" → "Web Service"
2. Connect your GitHub repository
3. Configure service:

```
Name: telegram-file-transfer-bot
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot_render.py
```

#### C. Add Environment Variables
In Render dashboard, go to Environment tab:

```
BOT_TOKEN=your_actual_bot_token_from_botfather
CREDENTIALS_PATH=./oauth_credentials.json
TOKEN_PATH=./token.json
```

#### D. Upload OAuth Files
1. Download `token.json` from your local machine (generated in Step 1A)
2. Download `oauth_credentials.json` from Google Cloud Console
3. Upload both files to your GitHub repository root

### Step 4: Test Deployment

#### A. Check Build Logs
- Monitor Render build logs for any errors
- Should see "✅ Google Drive connection established"

#### B. Test Bot Commands
1. Send `/start` - Should see welcome message
2. Send any file - Should upload to Google Drive
3. Check Google Drive for uploaded files

### Step 5: Monitor Usage

#### Free Tier Limits
- **750 hours/month** (31 days = 744 hours)
- **Bandwidth:** Unlimited
- **Storage:** Unlimited
- **Perfect for:** 24/7 bot operation

#### Auto-Sleep Behavior
- Free tier services sleep after 15 minutes of inactivity
- Wake up time: ~30 seconds
- **Tip:** Send a `/start` command to wake it up

### File Structure for Deployment

```
your-github-repo/
├── bot_render.py          # Main bot file
├── requirements.txt       # Python dependencies
├── render.yaml            # Render configuration
├── Procfile               # Startup command
├── oauth_credentials.json # OAuth client config
├── token.json             # OAuth tokens
└── README.md             # Documentation
```

### Troubleshooting

#### Build Errors
```bash
# Check Python version in render.yaml
# Ensure requirements.txt matches your local environment
```

#### OAuth Errors
- Verify `oauth_credentials.json` is uploaded
- Verify `token.json` is uploaded
- Check Google Cloud Console OAuth consent screen has test users

#### Bot Not Responding
- Check Render logs for errors
- Verify `BOT_TOKEN` environment variable is set
- Service may be sleeping (send `/start` to wake)

### Security Notes

✅ **Safe:** 
- Bot token is in environment variables
- OAuth credentials are stored securely
- No sensitive data in code

⚠️ **Remember:**
- Never commit `token.json` to public repos
- Use private repository for security
- Regenerate tokens if compromised

### Success! 🎉

Your bot will be available 24/7 at:
```
https://telegram-file-transfer-bot.onrender.com
```

Send `/start` to your bot on Telegram and watch it work in the cloud!