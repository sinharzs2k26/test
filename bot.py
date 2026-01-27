import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackContext

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    await update.message.reply_text("I'm a bot")

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handler
    application.add_handler(CommandHandler("start", start_command))
    
    # Check if running on Render
    is_render = 'RENDER' in os.environ

    # Start the bot with webhook
    if is_render:
        # Use webhook for Render
        port = int(os.environ.get('PORT', 10000))
        
        # Get webhook URL
        webhook_url = os.environ.get('RENDER_EXTERNAL_URL')
        if webhook_url:
            webhook_url = f"{webhook_url}/{TOKEN}"
            
            # Set custom handler for root path
            async def health_check(update: Update, context: CallbackContext):
                """Handle requests to root path"""
                await update.message.reply_text("✅ Bot is running!")

            # Start webhook
            application.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=TOKEN,  # Webhook listens on /TOKEN path
                webhook_url=webhook_url,
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )

if __name__ == "__main__":
    main()