import traceback
import html
import json
import logging
from datetime import datetime
import chatgpt

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram.constants import ParseMode

class handler:
    def __init__(self):
        self.HELP_MESSAGE = """
        Commands:
        /retry - Regenerate answer to the last prompt
        /new - Start new dialogue
        /mode - Select chat mode
        /balance - Show balance
        /help = Show help
        """
        self.logger = logging.getLogger(__name__)

    async def ping(self, update: Update, context: CallbackContext):
        reply_text = "Hi! I'm AssistGPT! How can i help you today?\n\n"
        reply_text += self.HELP_MESSAGE

        reply_text += "\nAsk me anything!"
        await update.message.reply_text(reply_text, parse_mode=ParseMode.HTML)

    async def help(self, update: Update, context: CallbackContext):
        await update.message.reply_text(self.HELP_MESSAGE, parse_mode=ParseMode.HTML)

    async def new_chat(self, update: Update, context: CallbackContext):
        await update.message.reply_text("Starting new chat!")

        bot_mode = "assistant" # retrieve the bot mode belonging to the user later
        await update.message.reply_text(chatgpt.BOT_MODES[bot_mode]["intro"], parse_mode=ParseMode.HTML)

    async def text_message(self, update: Update, context: CallbackContext, message=None, use_new_dialog_timeout=True):
        if update.edited_message is not None:
            # do something about it
            return
    
        if use_new_dialog_timeout:
            # check if the last interaction has timedout. If yes, then await update.message.reply_text("Starting new dialog due to timeout")
            pass

        try:
            bot_mode = "assistant" # fetch the user's preference from database
            prev_dialog = [] # fetch current session's previous dialogues

            message = message or update.message.text
            print(f'prompting for: {message[:50]}')
            gpt = chatgpt.ChatGPT()

            await update.message.chat.send_action(action="typing")
            answer, n_used_tokens, removed_n_dialog = gpt.send_message(message, dialog=prev_dialog, bot_mode=bot_mode)

            print(f'Used {n_used_tokens} tokens to generate response: {answer}')
            # new_dialog_message = {"user": message, "bot": "answer", "date": datetime.now()}
            # save the new dialog to user's session
            
        except Exception as e:
            self.logger.error(e)
            return update.message.reply_text('Generation failed. Please try again later.')
    
        if removed_n_dialog > 0:
            text = f"<i>Note</i> Your current dialog is too long, so <b>{removed_n_dialog} initial message(s)</b> were removed from the context.\nSend /new command to start new dialog"
            await update.message.reply_text(text, parse_mode=ParseMode.HTML)
        try:
            await update.message.reply_text(answer, parse_mode=ParseMode.HTML)
        except BadRequest:
            # Answer has invalid characters so we send it without parse_mode
            await update.message.reply_text(answer)

    async def show_bot_modes(self, update: Update, context: CallbackContext):
        keyboard = []
        for key, value in chatgpt.BOT_MODES.items():
            keyboard.append([InlineKeyboardButton(value["name"], callback_data=f'set_bot_mode|{key}')])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text("Select bot mode: ", reply_markup=reply_markup)

    async def set_bot_mode(self, update: Update, context: CallbackContext):
        query = update.callback_query
        await query.answer()

        bot_mode = query.data.split("|")[1]

        await query.edit_message_text(
        f"<b>{chatgpt.BOT_MODES[bot_mode]['name']}</b> Enabled!",
            parse_mode=ParseMode.HTML
        )

        await query.edit_message_text(f"{chatgpt.BOT_MODES[bot_mode]['intro']}", parse_mode=ParseMode.HTML)


    async def error(self, update: Update, context: CallbackContext):
        self.logger.error(msg="Exception while handling an update: ", exc_info=context.error)

        try:
            update_str = update.to_dict() if isinstance(update, Update) else str(update)
            message = (
                "An exception was raised while handling an update\n"
                f"<pre> update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n\n"
            )

            # split text into multiple messages due to 4096 character limit
            message_chunk_size = 4000
            message_chunks = [message[i:i+message_chunk_size] for i in range(0, len(message), message_chunk_size)]

            for message_chunk in message_chunks:
                await context.bot.send_message(update.effective_chat.id, message_chunk, parse_mode=ParseMode.HTML)

        except:
            await context.bot.send_message(update.effective_chat.id, "Some error in error handler")