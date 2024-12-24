import os
from telegram import Update, InlineQueryResultDocument
from telegram.ext import ApplicationBuilder, CommandHandler, InlineQueryHandler, CallbackContext

# Replace with your bot token
TOKEN = "7837107547:AAFHxOOOwSEG_AmCMr38MdZshhMe6GJOdGg"

# Movie directory
MOVIE_DIR = "movies"  # Directory where movies are stored

# Start command
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome! Use @pixlla_movies_bot <movie name> to search for movies inline.")

# Inline query handler
async def inline_query(update: Update, context: CallbackContext) -> None:
    query = update.inline_query.query.lower()

    # Check if movie directory exists
    if not os.path.exists(MOVIE_DIR):
        await update.inline_query.answer([], cache_time=0)
        return

    # Search for matching files
    files = os.listdir(MOVIE_DIR)
    matching_movies = [f for f in files if query in f.lower()]

    results = []
    for i, movie_file in enumerate(matching_movies):
        movie_path = os.path.join(MOVIE_DIR, movie_file)
        results.append(
            InlineQueryResultDocument(
                id=str(i),
                title=movie_file,
                document_url=f"file://{os.path.abspath(movie_path)}",
                mime_type="application/octet-stream",  # Generic file type
                description=f"Send {movie_file}"
            )
        )

    # Respond to the inline query
    await update.inline_query.answer(results, cache_time=0)

# Main function
def main() -> None:
    # Initialize the application
    application = ApplicationBuilder().token(TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(InlineQueryHandler(inline_query))

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
