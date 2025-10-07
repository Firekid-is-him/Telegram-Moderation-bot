from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only

@admin_only
async def pin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to pin it.")
        return
    
    try:
        await context.bot.pin_chat_message(
            update.effective_chat.id,
            update.message.reply_to_message.message_id
        )
        await update.message.reply_text("📌 Message pinned!")
    except Exception as e:
        await update.message.reply_text(f"Failed to pin message: {str(e)}")

@admin_only
async def unpin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.unpin_chat_message(update.effective_chat.id)
        await update.message.reply_text("📌 Message unpinned!")
    except Exception as e:
        await update.message.reply_text(f"Failed to unpin message: {str(e)}")

@admin_only
async def unpin_all(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.unpin_all_chat_messages(update.effective_chat.id)
        await update.message.reply_text("📌 All messages unpinned!")
    except Exception as e:
        await update.message.reply_text(f"Failed to unpin all messages: {str(e)}")
