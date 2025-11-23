# 🌐 Quick Render Setup
## Prepare Your Bot for Cloud Deployment

### ⚡ Fast Track Setup (5 Minutes)

#### Step 1: Generate OAuth Token
```bash
# Generate token.json for cloud deployment
python generate_render_token.py

# Choose option 1 to generate new token
```

#### Step 2: Create Repository
```bash
# Initialize Git repository
git init

# Add all files
git add .

# Commit
git commit -m "Telegram Bot - Render Ready"

# Create repo on GitHub and push
git remote add origin https://github.com/yourusername/telegram-bot.git
git push -u origin main
```

#### Step 3: Deploy on Render
1. Go to [render.com](https://render.com) and sign in
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:

```
Name: telegram-file-transfer-bot
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot_render.py
```

5. Add Environment Variables:

```
BOT_TOKEN=your_actual_bot_token_here
CREDENTIALS_PATH=./oauth_credentials.json
TOKEN_PATH=./token.json
```

#### Step 4: Test
- Wait for build to complete (2-3 minutes)
- Send `/start` to your bot
- Upload a file to test Google Drive connection

### 📁 Required Files (All included)

✅ `bot_render.py` - Cloud-optimized bot
✅ `requirements.txt` - Python dependencies  
✅ `render.yaml` - Render configuration
✅ `Procfile` - Startup command
✅ `generate_render_token.py` - Token generator
✅ `oauth_credentials.json` - Your OAuth config
✅ `token.json` - Generated token

### 🎯 What Makes This Cloud-Ready?

🔧 **Environment Variables** - Secure bot token storage
🔧 **OAuth Token Management** - Persistent authentication
🔧 **Cloud Logging** - Better error tracking
🔧 **Auto-Recovery** - Restarts on failures
🔧 **Health Checks** - Monitors service health

### 📊 Free Tier Benefits

🆓 **750 hours/month** (enough for 24/7 operation)
🆓 **Unlimited bandwidth**
🆓 **Unlimited storage**
🆓 **Automatic SSL certificates**
🆓 **Global CDN**

### ⚠️ Important Notes

1. **Repository Privacy**: Use private repository to protect your OAuth credentials
2. **Token Security**: Don't share your token.json file
3. **Sleep Behavior**: Bot sleeps after 15 minutes, wakes up in 30 seconds
4. **Monitor Usage**: Check Render dashboard for usage statistics

### 🚨 Troubleshooting

**Build Fails?**
- Check `requirements.txt` syntax
- Verify Python version compatibility

**Bot Not Responding?**
- Check Render logs for errors
- Verify environment variables are set
- Service may be sleeping (send `/start`)

**OAuth Errors?**
- Ensure both `oauth_credentials.json` and `token.json` are uploaded
- Verify Google Cloud Console OAuth consent screen settings

### 🎉 Success!

Once deployed, your bot runs 24/7 in the cloud:
- No more laptop required
- Faster processing speeds
- Always available
- Professional hosting

**Bot URL**: `https://telegram-file-transfer-bot.onrender.com`

Start using your bot anywhere, anytime! 🚀