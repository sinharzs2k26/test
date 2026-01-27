import os
import asyncio
import socket
import time
from threading import Thread
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN', 'YOUR_BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    await update.message.reply_text("I'm a bot")

def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(TOKEN).build()
    
    # Add command handler
    application.add_handler(CommandHandler("start", start_command))
  
    # Add this at the top of your main function
    def bind_to_port():
        """Bind to Render's required port (for web services)"""
        port = int(os.environ.get("PORT", 10000))
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('0.0.0.0', port))
            s.listen(1)
            print(f"✅ Port {port} bound successfully")
            
            # Keep the socket open
            while True:
                time.sleep(60)
    
    # Start port binding in a separate thread
    port_thread = Thread(target=bind_to_port, daemon=True)
    port_thread.start()

    # Then start your bot
    application.run_polling(
        drop_pending_updates=True,
        allowed_updates=Update.ALL_TYPES
    )

if __name__ == "__main__":
    main()