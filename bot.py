import os
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackContext

# Replace with your bot token
TOKEN = " 7837107547:AAFHxOOOwSEG_AmCMr38MdZshhMe6GJOdGg"

# Initialize Flask app
app = Flask(__name__)

# Telegram bot start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Use /movie <movie_name> to get a movie.")

# Telegram bot movie command
async def movie(update: Update, context: CallbackContext) -> None:
    if context.args is None or len(context.args) == 0:
        await update.message.reply_text("Please provide a movie name. Example: /movie Inception")
        return
    
    movie_name = " ".join(context.args).lower()
    movie_dir = "movies"  # Directory where movies are stored

    if not os.path.exists(movie_dir):
        await update.message.reply_text("Movie directory not found. Please contact the administrator.")
        return

    # Search for the movie file
    files = os.listdir(movie_dir)
    movie_file = next((f for f in files if movie_name in f.lower()), None)

    if movie_file:
        movie_path = os.path.join(movie_dir, movie_file)
        await update.message.reply_text(f"Sending {movie_file}...")
        with open(movie_path, 'rb') as movie:
            await context.bot.send_document(chat_id=update.message.chat_id, document=movie)
    else:
        await update.message.reply_text("Movie not found. Please try another title.")

# Flask route to handle webhook
@app.route('/' + TOKEN, methods=['POST'])
def webhook():
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("movie", movie))
    return 'OK'

if __name__ == '__main__':
    # Get the port from environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
