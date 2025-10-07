from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only

@admin_only
async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        await update.message.reply_text("Please reply to a message to delete it.")
        return
    
    try:
        await update.message.reply_to_message.delete()
        await update.message.reply_text("✅ Message deleted!")
    except Exception as e:
        await update.message.reply_text(f"Failed to delete message: {str(e)}")

@admin_only
async def purge_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /purge <number>")
        return
    
    try:
        count = int(context.args[0])
        if count < 1 or count > 100:
            await update.message.reply_text("Please provide a number between 1 and 100.")
            return
    except ValueError:
        await update.message.reply_text("Please provide a valid number.")
        return
    
    chat_id = update.effective_chat.id
    message_id = update.message.message_id
    deleted = 0
    
    try:
        for i in range(1, count + 1):
            try:
                await context.bot.delete_message(chat_id, message_id - i)
                deleted += 1
            except:
                pass
        
        msg = await update.message.reply_text(f"🗑 Deleted {deleted} messages!")
        await msg.delete()
        await update.message.delete()
    except Exception as e:
        await update.message.reply_text(f"Failed to purge messages: {str(e)}")
