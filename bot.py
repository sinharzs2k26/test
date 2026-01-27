import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command"""
    await update.message.reply_text("I'm a bot")
    
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Bot is active! Use @locdev26_bot on Telegram.')
    
    def log_message(self, format, *args):
        # Disable logging
        pass

def start_health_server():
    """Start a simple HTTP server for health checks"""
    port = int(os.getenv('PORT', 10000))
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    server.serve_forever()
    
def main():
    """Start the bot"""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add command handler
    application.add_handler(CommandHandler("start", start_command))
    
    # Start health server in background thread
    health_thread = threading.Thread(target=start_health_server, daemon=True)
    health_thread.start()
    
    # Start the bot
    # Check if running on Render
    is_render = 'RENDER' in os.environ
    
    if is_render:
        # Use webhook for Render
        port = int(os.getenv('PORT', 10000))
        
        # Get webhook URL
        webhook_url = os.environ.get('RENDER_EXTERNAL_URL')
        if webhook_url:
            # Set webhook URL with token
            webhook_url = f"{webhook_url}/{TOKEN}"
            # Start webhook
            application.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=TOKEN,
                webhook_url=webhook_url,
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
        else:
            application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
    else:
        # Use polling for local development
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )

if __name__ == "__main__":
    main()