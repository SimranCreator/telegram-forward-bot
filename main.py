import json
from telegram import Update, Bot
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext

with open("config.json") as f:
    config = json.load(f)

BOT_TOKEN = config["8878054728:AAHc8VcHuVmPCHE_mJxXWypDA5hRKaGhazwE"]
SOURCE_CHATS = config["@DevelopmentNewsIndia"]
TARGET_CHAT = config["@warupdatenow]
WATERMARK = config["simrancreator"]

mode = config["mode"]

def save_mode(new_mode):
    config["mode"] = new_mode
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Bot is running.\n\n"
        "/allmessages – Forward everything\n"
        "/photosonly – Forward only photos/videos"
    )

def set_all(update: Update, context: CallbackContext):
    save_mode("all")
    update.message.reply_text("Mode changed: Forwarding ALL messages.")

def set_media(update: Update, context: CallbackContext):
    save_mode("media")
    update.message.reply_text("Mode changed: Forwarding only photos/videos.")

def process(update: Update, context: CallbackContext):
    message = update.effective_message

    if str(message.chat.username) not in [s.replace("@", "") for s in SOURCE_CHATS]:
        return

    if config["mode"] == "media":
        if not (message.photo or message.video):
            return

    if message.text:
        text = f"{message.text}\n\n{WATERMARK}"
        context.bot.send_message(chat_id=TARGET_CHAT, text=text)
        return

    if message.photo:
        file = message.photo[-1].file_id
        caption = (message.caption or "") + f"\n\n{WATERMARK}"
        context.bot.send_photo(chat_id=TARGET_CHAT, photo=file, caption=caption)
        return

    if message.video:
        file = message.video.file_id
        caption = (message.caption or "") + f"\n\n{WATERMARK}"
        context.bot.send_video(chat_id=TARGET_CHAT, video=file, caption=caption)
        return

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", start))
dp.add_handler(CommandHandler("allmessages", set_all))
dp.add_handler(CommandHandler("photosonly", set_media))
dp.add_handler(MessageHandler(Filters.all, process))

updater.start_polling()
print("Bot is running…")
