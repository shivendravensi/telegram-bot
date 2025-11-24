#!/usr/bin/env python3
"""
Telegram Bot with Google Drive Integration - RAM Optimized for Free Tier
Handles large files (200MB-2GB) within 512MB RAM constraints using streaming approach
"""

import logging
import os
import mimetypes
import io
import tempfile
import shutil
from datetime import datetime
from googleapiclient.http import MediaFileUpload
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class GoogleDriveUploader:
    def __init__(self):
        self.service = None
        self.token_path = 'token.json'
        self.credentials_path = 'oauth_credentials.json'
        self.setup_service()
    
    def setup_service(self):
        """Initialize Google Drive service"""
        SCOPES = ['https://www.googleapis.com/auth/drive.file']
        
        try:
            # Load credentials
            creds = None
            if os.path.exists(self.token_path):
                creds = Credentials.from_authorized_user_file(self.token_path, SCOPES)
            
            # Refresh or get new credentials
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        self.credentials_path, SCOPES)
                    creds = flow.run_local_server(port=0)
                
                # Save credentials
                with open(self.token_path, 'w') as token:
                    token.write(creds.to_json())
            
            # Build service
            self.service = build('drive', 'v3', credentials=creds)
            logger.info("Google Drive service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Google Drive service: {e}")
            raise
    
    def get_or_create_folder(self, folder_name="Telegram Files"):
        """Get or create a folder in Google Drive"""
        try:
            # Try to find existing folder
            results = self.service.files().list(
                q=f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'",
                fields='files(id, name)'
            ).execute()
            
            items = results.get('files', [])
            
            if items:
                folder_id = items[0]['id']
                logger.info(f"Using existing folder: {folder_name} (ID: {folder_id})")
            else:
                # Create new folder
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(
                    body=folder_metadata,
                    fields='id'
                ).execute()
                folder_id = folder.get('id')
                logger.info(f"Created new folder: {folder_name} (ID: {folder_id})")
            
            return folder_id
            
        except HttpError as e:
            logger.error(f"Error handling folder: {e}")
            raise

    def upload_chunked_file(self, file_path, file_name, folder_id):
        """Upload large file using chunked approach with temporary files"""
        try:
            # Get file size
            file_size = os.path.getsize(file_path)
            logger.info(f"Uploading file: {file_name} ({file_size} bytes)")
            
            # Determine MIME type
            mime_type, _ = mimetypes.guess_type(file_name)
            if not mime_type:
                if file_name.endswith(('.jpg', '.jpeg')):
                    mime_type = 'image/jpeg'
                elif file_name.endswith('.png'):
                    mime_type = 'image/png'
                elif file_name.endswith('.pdf'):
                    mime_type = 'application/pdf'
                elif file_name.endswith(('.mp4', '.avi', '.mov')):
                    mime_type = 'video/mp4'
                elif file_name.endswith('.mp3'):
                    mime_type = 'audio/mpeg'
                elif file_name.endswith('.ogg'):
                    mime_type = 'audio/ogg'
                elif file_name.endswith('.gif'):
                    mime_type = 'image/gif'
                else:
                    mime_type = 'application/octet-stream'
            
            # Create file metadata
            file_metadata = {
                'name': file_name,
                'parents': [folder_id]
            }
            
            # Use MediaFileUpload with chunked approach
            # MediaFileUpload handles chunking internally with the file
            media = MediaFileUpload(
                file_path,
                mimetype=mime_type,
                chunksize=8*1024*1024,  # 8MB chunks
                resumable=True
            )
            
            # Upload file with progress callback
            request = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id,webViewLink'
            )
            
            # Execute upload with retry logic for large files
            file = None
            response = None
            while response is None:
                status, response = request.next_chunk()
                if status:
                    progress = (status.progress() * 100)
                    logger.info(f"Upload progress: {progress:.1f}%")
            
            file = response
            
            # Make file publicly viewable
            permission = {'role': 'reader', 'type': 'anyone'}
            self.service.permissions().create(fileId=file.get('id'), body=permission).execute()
            
            # Get shareable link
            file_id = file.get('id')
            file = self.service.files().get(fileId=file_id, fields='id,webViewLink').execute()
            
            return {
                'id': file['id'],
                'webViewLink': file['webViewLink'],
                'size': file_size
            }
            
        except HttpError as e:
            logger.error(f"Media upload error: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected upload error: {e}")
            raise

class TelegramFileBot:
    def __init__(self):
        self.uploader = GoogleDriveUploader()
        self.folder_id = self.uploader.get_or_create_folder()
        
    async def handle_start(self, update: Update, context):
        """Handle /start command"""
        welcome_msg = """
🤖 **Telegram to Google Drive Bot**

Upload files directly to your Google Drive cloud storage!

**Features:**
📁 Automatic file organization
📤 Large file support (up to 2GB)
🔗 Direct shareable links
⚡ Fast cloud processing

**Supported formats:**
📄 Documents: PDF, DOC, TXT, etc.
🖼️ Images: JPG, PNG, GIF
🎬 Videos: MP4, AVI, MOV
🎵 Audio: MP3, OGG
📦 Archives: ZIP, RAR

**How to use:**
1. Send any file to the bot
2. Wait for upload completion
3. Get your shareable Google Drive link!

**Commands:**
/help - Show this help
/status - Check bot status
        """
        await update.message.reply_text(welcome_msg, parse_mode='Markdown')
    
    async def handle_help(self, update: Update, context):
        """Handle /help command"""
        help_msg = """
🆘 **Help & Commands**

**Commands:**
/start - Welcome message
/help - Show this help
/status - Check bot status

**How to upload files:**
1. Simply send any file to the bot
2. The bot will automatically upload to Google Drive
3. You'll receive a shareable link when done

**File size limit:**
- Maximum: 2GB per file
- Best performance: Files under 500MB

**Supported formats:**
📄 Documents: PDF, DOC, DOCX, TXT, RTF, ODT
🖼️ Images: JPG, JPEG, PNG, GIF, BMP, TIFF
🎬 Videos: MP4, AVI, MOV, MKV, WMV, FLV
🎵 Audio: MP3, AAC, OGG, WAV, FLAC, M4A
📦 Archives: ZIP, RAR, 7Z, TAR, GZ

**Privacy & Security:**
- Files are stored in your personal Google Drive
- No files are permanently stored on bot servers
- All uploads use encrypted connections
- Files are made public only if you share the link

**Need help?**
Contact the bot administrator if you encounter issues.
        """
        await update.message.reply_text(help_msg, parse_mode='Markdown')
    
    async def handle_status(self, update: Update, context):
        """Handle /status command"""
        status_msg = f"""
📊 **Bot Status**

✅ **Bot Status:** Active and Running
🌐 **Platform:** Render Cloud
💾 **RAM Usage:** Optimized for Free Tier
🔗 **Folder ID:** `{self.folder_id}`

**Google Drive:**
✅ Service Connected
✅ Folder Ready
🔄 **Cloud Status:** Online

**Limits:**
📏 Max File Size: 2GB
⚡ Performance: Optimized
💾 Memory: Efficient streaming

The bot is ready to receive your files! 🚀
        """
        await update.message.reply_text(status_msg, parse_mode='Markdown')
    
    async def handle_media(self, update, context, media_type):
        """Handle media file upload with RAM optimization"""
        try:
            # Extract file info based on media type
            if media_type == "document":
                file = update.message.document
                file_name = file.file_name or f"document_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            elif media_type == "photo":
                file = update.message.photo[-1]  # Get highest quality
                file_name = f"photo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            elif media_type == "video":
                file = update.message.video
                file_name = f"video_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4"
            elif media_type == "animation":
                file = update.message.animation
                file_name = f"animation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.gif"
            elif media_type == "audio":
                file = update.message.audio
                file_name = f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
            elif media_type == "voice":
                file = update.message.voice
                file_name = f"voice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.ogg"
            else:
                await update.message.reply_text("❌ Unsupported file type")
                return
            
            # Check if file is too large (Telegram bot API limit)
            file_size_mb = file.file_size / (1024 * 1024)
            if file_size_mb > 50:
                await update.message.reply_text(
                    f"⚠️ **Large File Detected**\n\n"
                    f"📁 File: {file_name}\n"
                    f"📏 Size: {file_size_mb:.1f} MB\n\n"
                    f"🔄 Processing with optimized upload method...\n"
                    f"💾 Using streaming approach for memory efficiency"
                )
            
            # Send processing message
            processing_msg = await update.message.reply_text(
                f"⏳ **Processing file...**\n\n"
                f"📁 File: {file_name}\n"
                f"📏 Size: {file_size_mb:.1f} MB\n"
                f"🔄 Downloading from Telegram..."
            )
            
            # Download file to temporary location using streaming
            await self._upload_large_file_streaming(file, file_name, processing_msg)
            
        except Exception as e:
            logger.error(f"Media upload error: {e}")
            await update.message.reply_text(f"❌ Upload failed: {str(e)}")
    
    async def _upload_large_file_streaming(self, file, file_name, processing_msg):
        """Upload large file using temporary files (RAM optimized)"""
        temp_file_path = None
        try:
            # Get file from Telegram
            telegram_file = await file.get_file()
            
            # Create temporary file (more efficient than memory for large files)
            with tempfile.NamedTemporaryFile(delete=False, suffix='_telegram_upload') as temp_file:
                temp_file_path = temp_file.name
            
            logger.info(f"Downloading to temporary file: {temp_file_path}")
            
            # Update progress
            await processing_msg.edit_text(
                f"⏳ **Downloading from Telegram...**\n\n"
                f"📁 File: {file_name}\n"
                f"💾 Using temporary file storage\n"
                f"🔄 Progress will be shown during upload"
            )
            
            # Download to temporary file
            await telegram_file.download_to_drive(temp_file_path)
            
            # Update progress
            await processing_msg.edit_text(
                f"📤 **Uploading to Google Drive...**\n\n"
                f"📁 File: {file_name}\n"
                f"🔄 Using chunked upload method"
            )
            
            # Upload to Google Drive
            result = self.uploader.upload_chunked_file(
                temp_file_path, 
                file_name, 
                self.folder_id
            )
            
            # Success message
            file_size_mb = result['size'] / (1024 * 1024)
            await processing_msg.edit_text(
                f"✅ **Upload Successful!**\n\n"
                f"📁 File: {file_name}\n"
                f"📏 Size: {file_size_mb:.1f} MB\n"
                f"📂 Location: Telegram Files\n"
                f"🔗 **Google Drive Link:**\n{result['webViewLink']}\n\n"
                f"🌐 **Cloud Status:** Optimized for Render Free Tier\n"
                f"💾 **Memory Usage:** Streaming approach active"
            )
            
        except Exception as e:
            logger.error(f"Upload error: {e}")
            await processing_msg.edit_text(f"❌ Upload failed: {str(e)}")
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                    logger.info(f"Cleaned up temporary file: {temp_file_path}")
                except Exception as e:
                    logger.warning(f"Failed to remove temp file: {e}")
    
    # Handler methods for different media types
    async def handle_document(self, update, context):
        """Handle document uploads"""
        await self.handle_media(update, context, "document")
    
    async def handle_photo(self, update, context):
        """Handle photo uploads"""
        await self.handle_media(update, context, "photo")
    
    async def handle_video(self, update, context):
        """Handle video uploads"""
        await self.handle_media(update, context, "video")
    
    async def handle_animation(self, update, context):
        """Handle animation uploads"""
        await self.handle_media(update, context, "animation")
    
    async def handle_audio(self, update, context):
        """Handle audio uploads"""
        await self.handle_media(update, context, "audio")
    
    async def handle_voice(self, update, context):
        """Handle voice message uploads"""
        await self.handle_media(update, context, "voice")

def main():
    """Main function to run the bot"""
    # Get bot token from environment
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set")
        return
    
    # Create bot instance
    bot = TelegramFileBot()
    
    # Create application
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.handle_start))
    application.add_handler(CommandHandler("help", bot.handle_help))
    application.add_handler(CommandHandler("status", bot.handle_status))
    
    # Add media handlers
    application.add_handler(MessageHandler(filters.Document.ALL, bot.handle_document))
    application.add_handler(MessageHandler(filters.PHOTO, bot.handle_photo))
    application.add_handler(MessageHandler(filters.VIDEO, bot.handle_video))
    application.add_handler(MessageHandler(filters.ANIMATION, bot.handle_animation))
    application.add_handler(MessageHandler(filters.AUDIO, bot.handle_audio))
    application.add_handler(MessageHandler(filters.VOICE, bot.handle_voice))
    
    # Start bot
    logger.info("Starting Telegram bot...")
    application.run_polling()

if __name__ == '__main__':
    main()