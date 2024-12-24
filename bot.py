from flask import Flask, request
from telegram import Update
from telegram.ext import Dispatcher, CommandHandler, Updater

app = Flask(_name_)

# Replace with your bot token
TOKEN = "7837107547:AAFHxOOOwSEG_AmCMr38MdZshhMe6GJOdGg"
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Define your commands (e.g., start command)
def start(update, context):
    context.bot.send_message(chat_id=update.message.chat_id, text="Hello! I'm your movie bot.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Webhook route to receive updates from Telegram
@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = Update.de_json(json_str, updater.bot)
    dispatcher.process_update(update)
    return 'ok'

if _name_ == '_main_':
    app.run(debug=True, port=5000)
