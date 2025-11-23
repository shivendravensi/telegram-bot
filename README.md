# 🤖 Telegram to Google Drive Bot

A powerful Telegram bot that transfers files to Google Drive for fast, unlimited downloads. **Optimized for cloud deployment on Render.**

## 🚀 Features

✅ **Single File Upload** - Photos, videos, documents, audio, voice messages  
✅ **Bulk Channel Download** - Download entire channels with range selection  
✅ **Automatic Organization** - Creates folders by channel name  
✅ **Cloud Deployment Ready** - Runs 24/7 on Render (750 hours/month FREE)  
✅ **Multi-Media Support** - Handles all Telegram media types  
✅ **Forward Message Support** - Downloads forwarded media automatically  

## 📱 Commands

### Single File Upload
Simply send any file directly to the bot

### Bulk Download
```
/bulk @channel_name                    # Download all media
/bulk @channel_name limit=10          # Latest 10 files
/bulk @channel_name days=7            # Last 7 days
/bulk @channel_name photos_only       # Only images
/bulk @channel_name videos_only       # Only videos
/bulk @channel_name limit=20 videos_only  # 20 latest videos
```

### Bot Commands
```
/start     - Welcome message
/help      - Help and commands
/status    - Bot status and info
```

## 🌐 Cloud Deployment (Render)

### Free Tier Benefits
- **750 hours/month** (24/7 operation)
- **Unlimited bandwidth**
- **Unlimited storage**
- **Auto SSL certificates**
- **Global CDN**

### Deployment Steps

1. **Generate OAuth Token**
   ```bash
   python generate_render_token.py
   ```

2. **Create GitHub Repository**
   ```bash
   git init
   git add .
   git commit -m "Telegram Bot - Render Ready"
   git remote add origin https://github.com/yourusername/telegram-bot.git
   git push -u origin main
   ```

3. **Deploy on Render**
   - Go to [render.com](https://render.com)
   - New → Web Service → Connect GitHub
   - Configure service:
     ```
     Runtime: Python 3
     Build Command: pip install -r requirements.txt
     Start Command: python bot_render.py
     ```

4. **Set Environment Variables**
   ```
   BOT_TOKEN=your_bot_token_here
   CREDENTIALS_PATH=./oauth_credentials.json
   TOKEN_PATH=./token.json
   ```

5. **Upload OAuth Files**
   - Upload `oauth_credentials.json` to repository
   - Upload `token.json` to repository

### File Structure
```
├── bot_render.py              # Main bot file (cloud-optimized)
├── requirements.txt           # Python dependencies
├── render.yaml               # Render configuration
├── Procfile                  # Startup command
├── oauth_credentials.json    # OAuth client config
├── token.json               # OAuth tokens
├── generate_render_token.py  # Token generator
├── RENDER_DEPLOYMENT_GUIDE.md # Detailed guide
├── QUICK_RENDER_SETUP.md     # Quick setup
└── README.md                 # This file
```

## 🔧 Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export BOT_TOKEN=your_bot_token_here

# Run locally
python bot_render.py
```

### OAuth Setup
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Drive API
3. Create OAuth 2.0 Client ID (Desktop Application)
4. Download as `oauth_credentials.json`
5. Run: `python generate_render_token.py`

## 📊 Features Comparison

| Feature | Local Bot | Render Bot |
|---------|-----------|------------|
| 24/7 Operation | ❌ (laptop required) | ✅ (free hosting) |
| Uptime | ❌ (manual restart) | ✅ (auto-restart) |
| Performance | ⚠️ (variable) | ✅ (optimized) |
| Accessibility | ❌ (local only) | ✅ (anywhere) |
| Maintenance | ⚠️ (manual) | ✅ (automated) |

## 🔒 Security

- ✅ Bot tokens stored in environment variables
- ✅ OAuth credentials protected
- ✅ No sensitive data in code
- ⚠️ Use private GitHub repository for OAuth files

## 📈 Usage Statistics

### Processing Times
- **Photos (1-5MB)**: 5-10 seconds
- **Videos (100-500MB)**: 2-5 minutes  
- **Large files (1GB+)**: 5-13 minutes
- **Bulk downloads**: Significantly faster with server-side processing

### Cost Analysis
- **Telegram Direct**: Free but slow (1GB = 20-30 minutes)
- **Google Drive**: 15GB free storage, unlimited bandwidth
- **Render Hosting**: Free (750 hours/month)
- **Total Cost**: $0/month

## 🆘 Support

### Common Issues

**Bot not responding?**
- Check Render logs
- Verify environment variables
- Service may be sleeping (send `/start`)

**OAuth errors?**
- Ensure `oauth_credentials.json` is uploaded
- Verify `token.json` exists
- Check Google Cloud Console OAuth settings

**Build failures?**
- Check `requirements.txt` syntax
- Verify Python version compatibility
- Review build logs

### Documentation
- 📘 [Detailed Deployment Guide](RENDER_DEPLOYMENT_GUIDE.md)
- ⚡ [Quick Setup Guide](QUICK_RENDER_SETUP.md)
- 🔧 [Local Development](generate_render_token.py)

## 🎯 Benefits Summary

✅ **No Laptop Required** - Runs 24/7 in the cloud  
✅ **Faster Downloads** - Server-side processing  
✅ **Always Available** - No downtime  
✅ **Free Forever** - 750 hours/month on Render  
✅ **Professional** - SSL, CDN, monitoring included  
✅ **Scalable** - Handles multiple users  
✅ **Secure** - Environment variables, OAuth protection  

## 🚀 Get Started

1. **Fork/Clone** this repository
2. **Generate OAuth token**: `python generate_render_token.py`
3. **Create GitHub repo** and push files
4. **Deploy to Render** following the guide
5. **Start using** your 24/7 bot!

**Ready to deploy? Start with [QUICK_RENDER_SETUP.md](QUICK_RENDER_SETUP.md)** 🎉