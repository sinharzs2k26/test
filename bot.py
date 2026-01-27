import os
import threading
import http.server
import socketserver
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
    
    # Check if running on Render
    is_render = 'RENDER' in os.environ

    if is_render:
        port = int(os.environ.get('PORT', 10000))
        webhook_url = os.environ.get('RENDER_EXTERNAL_URL')
        
        if webhook_url:
            webhook_url = f"{webhook_url}/{TOKEN}"
            
            # ====== ADD THIS: Set up simple response handler ======
            class DualHandler(http.server.BaseHTTPRequestHandler):
                def do_GET(self):
                    if self.path == '/':
                        self.send_response(200)
                        self.send_header('Content-type', 'text/plain')
                        self.end_headers()
                        self.wfile.write(b'✅ Bot is active!')
                    else:
                        self.send_response(404)
                        self.end_headers()
                
                def log_message(self, format, *args):
                    pass
            
            def run_health_server():
                with socketserver.TCPServer(("0.0.0.0", port), DualHandler) as httpd:
                    logger.info(f"✅ Serving on port {port}")
                    httpd.serve_forever()
            
            # Start in separate thread
            server_thread = threading.Thread(target=run_health_server, daemon=True)
            server_thread.start()
            # ====== END OF ADDITION ======
            
            # Start bot (it will fail to bind to port - so DON'T use this approach)
            # application.run_webhook(...)  # This will fail!
if __name__ == "__main__":
    main()