from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only, check_permission
from utils.storage import get_chat_data, save_chat_data

@admin_only
async def add_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /filter <keyword> <response>")
        return
    
    keyword = context.args[0].lower()
    response = ' '.join(context.args[1:])
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/filters.json', chat_id)
    
    if 'filters' not in data[chat_id_str]:
        data[chat_id_str]['filters'] = {}
    
    data[chat_id_str]['filters'][keyword] = response
    save_chat_data('data/filters.json', data)
    
    await update.message.reply_text(f"✅ Filter added for '{keyword}'!")

@check_permission('filters')
async def list_filters(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/filters.json', chat_id)
    
    filters = data[chat_id_str].get('filters', {})
    
    if not filters:
        await update.message.reply_text("No filters set for this group.")
        return
    
    filter_text = "<b>Active Filters</b>\n\n"
    for keyword in filters.keys():
        filter_text += f"• {keyword}\n"
    
    await update.message.reply_text(filter_text, parse_mode='HTML')

@admin_only
async def remove_filter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /stop <keyword>")
        return
    
    keyword = context.args[0].lower()
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/filters.json', chat_id)
    
    if 'filters' in data[chat_id_str] and keyword in data[chat_id_str]['filters']:
        del data[chat_id_str]['filters'][keyword]
        save_chat_data('data/filters.json', data)
        await update.message.reply_text(f"✅ Filter removed for '{keyword}'!")
    else:
        await update.message.reply_text(f"No filter found for '{keyword}'")

@admin_only
async def add_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /blacklist <word1> <word2> ...")
        return
    
    words = [word.lower() for word in context.args]
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/blacklist.json', chat_id)
    
    if 'words' not in data[chat_id_str]:
        data[chat_id_str]['words'] = []
    
    for word in words:
        if word not in data[chat_id_str]['words']:
            data[chat_id_str]['words'].append(word)
    
    save_chat_data('data/blacklist.json', data)
    await update.message.reply_text(f"✅ Added {len(words)} word(s) to blacklist!")

@admin_only
async def remove_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /unblacklist <word1> <word2> ...")
        return
    
    words = [word.lower() for word in context.args]
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/blacklist.json', chat_id)
    
    if 'words' in data[chat_id_str]:
        for word in words:
            if word in data[chat_id_str]['words']:
                data[chat_id_str]['words'].remove(word)
        save_chat_data('data/blacklist.json', data)
        await update.message.reply_text(f"✅ Removed word(s) from blacklist!")
    else:
        await update.message.reply_text("No blacklist found for this group.")

@check_permission('blacklisted')
async def show_blacklist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/blacklist.json', chat_id)
    
    words = data[chat_id_str].get('words', [])
    
    if not words:
        await update.message.reply_text("No blacklisted words for this group.")
        return
    
    blacklist_text = "<b>Blacklisted Words</b>\n\n"
    blacklist_text += ', '.join(words)
    
    await update.message.reply_text(blacklist_text, parse_mode='HTML')
