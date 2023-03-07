from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters

from handlers import handler
import config

if __name__ == "__main__":
    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).build()
    handler = handler()

    allowed_telegram_usernames = ["kushgabani"]
    if len(allowed_telegram_usernames) == 0:
        user_filter = filters.ALL
    else:
        user_filter = filters.User(username=allowed_telegram_usernames)


    app.add_handler(CommandHandler("ping", handler.ping, filters=user_filter))
    app.add_handler(CommandHandler("help", handler.help, filters=user_filter))
    app.add_handler(CommandHandler("new", handler.new_chat, filters=user_filter))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & user_filter, handler.text_message))
    app.add_handler(CommandHandler("mode", handler.show_bot_modes, filters=user_filter))
    app.add_handler(CallbackQueryHandler(handler.set_bot_mode, pattern='^set_bot_mode'))
    app.add_handler(CommandHandler("balance", handler.set_bot_mode, filters=user_filter))

    app.add_error_handler(handler.error)

    print("AssistGPT active and listening on Telegram")
    app.run_polling()
