import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
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

    class HealthHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Bot is alive!')
        
        def log_message(self, format, *args):
            pass  # Silence logs
    
    def run_health_server():
        port = int(os.environ.get("PORT", 8080))
        server = HTTPServer(('0.0.0.0', port), HealthHandler)
        print(f"✅ Health server on port {port}")
        server.serve_forever()
    
    # Start health server
    health_thread = threading.Thread(target=run_health_server, daemon=True)
    health_thread.start()
            
    # Start the bot
    print("Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()