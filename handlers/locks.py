from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only
from utils.storage import get_chat_data, save_chat_data

LOCK_TYPES = ['messages', 'media', 'stickers', 'links', 'polls', 'forwards']

@admin_only
async def lock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(f"Usage: /lock <type>\nAvailable types: {', '.join(LOCK_TYPES)}")
        return
    
    lock_type = context.args[0].lower()
    if lock_type not in LOCK_TYPES:
        await update.message.reply_text(f"Invalid type. Available: {', '.join(LOCK_TYPES)}")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/locks.json', chat_id)
    
    if 'locks' not in data[chat_id_str]:
        data[chat_id_str]['locks'] = []
    
    if lock_type not in data[chat_id_str]['locks']:
        data[chat_id_str]['locks'].append(lock_type)
    
    save_chat_data('data/locks.json', data)
    await update.message.reply_text(f"🔒 Locked {lock_type}!")

@admin_only
async def unlock(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(f"Usage: /unlock <type>\nAvailable types: {', '.join(LOCK_TYPES)}")
        return
    
    lock_type = context.args[0].lower()
    if lock_type not in LOCK_TYPES:
        await update.message.reply_text(f"Invalid type. Available: {', '.join(LOCK_TYPES)}")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/locks.json', chat_id)
    
    if 'locks' in data[chat_id_str] and lock_type in data[chat_id_str]['locks']:
        data[chat_id_str]['locks'].remove(lock_type)
    
    save_chat_data('data/locks.json', data)
    await update.message.reply_text(f"🔓 Unlocked {lock_type}!")

@admin_only
async def lockall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/locks.json', chat_id)
    
    data[chat_id_str]['locks'] = LOCK_TYPES.copy()
    save_chat_data('data/locks.json', data)
    await update.message.reply_text("🔒 Locked all message types!")

@admin_only
async def unlockall(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/locks.json', chat_id)
    
    data[chat_id_str]['locks'] = []
    save_chat_data('data/locks.json', data)
    await update.message.reply_text("🔓 Unlocked everything!")
