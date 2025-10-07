from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only, check_permission
from utils.helpers import get_user_from_message
from utils.storage import get_chat_data, save_chat_data

@check_permission('info')
async def get_user_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        target_user = update.effective_user
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to get their info.")
        return
    
    try:
        chat_member = await update.effective_chat.get_member(target_user.id)
        
        info_text = f"""
<b>User Information</b>

Name: {target_user.full_name}
ID: <code>{target_user.id}</code>
Username: @{target_user.username if target_user.username else 'None'}
Status: {chat_member.status}
"""
        await update.message.reply_text(info_text, parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to get user info: {str(e)}")

@check_permission('warns')
async def check_warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        target_user = update.effective_user
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to check their warnings.")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/warnings.json', chat_id)
    user_id_str = str(target_user.id)
    
    warnings = data[chat_id_str].get(user_id_str, [])
    
    if not warnings:
        await update.message.reply_text(f"{target_user.mention_html()} has no warnings.", parse_mode='HTML')
        return
    
    warn_text = f"<b>Warnings for {target_user.full_name}</b>\n\n"
    for i, warn in enumerate(warnings, 1):
        warn_text += f"{i}. {warn['reason']} - {warn['time'][:10]}\n"
    
    await update.message.reply_text(warn_text, parse_mode='HTML')

@admin_only
async def reset_warns(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to reset their warnings.")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/warnings.json', chat_id)
    user_id_str = str(target_user.id)
    
    if user_id_str in data[chat_id_str]:
        del data[chat_id_str][user_id_str]
        save_chat_data('data/warnings.json', data)
    
    await update.message.reply_text(f"✅ Warnings reset for {target_user.mention_html()}!", parse_mode='HTML')
