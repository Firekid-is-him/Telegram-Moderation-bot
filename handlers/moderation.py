from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only
from utils.helpers import get_user_from_message, parse_time
from utils.storage import get_chat_data, save_chat_data, read_json
from datetime import datetime, timedelta

@admin_only
async def warn_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to warn them.")
        return
    
    user_id = target_user.id
    
    if update.message.reply_to_message:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    elif context.args and context.args[0].startswith('@'):
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
    else:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    
    data, chat_id_str = get_chat_data('data/warnings.json', chat_id)
    user_id_str = str(user_id)
    
    if user_id_str not in data[chat_id_str]:
        data[chat_id_str][user_id_str] = []
    
    warn_data = {
        'reason': reason,
        'time': datetime.now().isoformat()
    }
    data[chat_id_str][user_id_str].append(warn_data)
    save_chat_data('data/warnings.json', data)
    
    warn_count = len(data[chat_id_str][user_id_str])
    max_warns = int(context.bot_data.get('max_warns', 3))
    
    await update.message.reply_text(
        f"⚠️ {target_user.mention_html()} has been warned!\n"
        f"Reason: {reason}\n"
        f"Warnings: {warn_count}/{max_warns}",
        parse_mode='HTML'
    )
    
    if warn_count >= max_warns:
        settings = read_json('data/settings.json')
        chat_settings = settings.get(chat_id_str, {})
        action_type = chat_settings.get('maxwarn_action', 'ban')
        
        if action_type == 'ban':
            await context.bot.ban_chat_member(chat_id, user_id)
            await update.message.reply_text(f"🚫 {target_user.mention_html()} has been banned for reaching max warnings!", parse_mode='HTML')
        elif action_type == 'kick':
            await context.bot.ban_chat_member(chat_id, user_id)
            await context.bot.unban_chat_member(chat_id, user_id)
            await update.message.reply_text(f"👢 {target_user.mention_html()} has been kicked for reaching max warnings!", parse_mode='HTML')
        elif action_type.startswith('tempban'):
            duration = chat_settings.get('maxwarn_duration', 3600)
            until_date = datetime.now() + timedelta(seconds=duration)
            await context.bot.ban_chat_member(chat_id, user_id, until_date=until_date)
            await update.message.reply_text(f"⏱ {target_user.mention_html()} has been temp banned for reaching max warnings!", parse_mode='HTML')

@admin_only
async def kick_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to kick them.")
        return
    
    if update.message.reply_to_message:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    elif context.args and context.args[0].startswith('@'):
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
    else:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await context.bot.unban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"👢 {target_user.mention_html()} has been kicked!\nReason: {reason}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to kick user: {str(e)}")

@admin_only
async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to ban them.")
        return
    
    if update.message.reply_to_message:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    elif context.args and context.args[0].startswith('@'):
        reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "No reason provided"
    else:
        reason = ' '.join(context.args) if context.args else "No reason provided"
    
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"🚫 {target_user.mention_html()} has been banned!\nReason: {reason}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to ban user: {str(e)}")

@admin_only
async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to unban them.")
        return
    
    try:
        await context.bot.unban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"✅ {target_user.mention_html()} has been unbanned!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to unban user: {str(e)}")

@admin_only
async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to mute them.")
        return
    
    duration = None
    if len(context.args) > 1:
        duration = parse_time(context.args[1])
    
    try:
        if duration:
            until_date = datetime.now() + timedelta(seconds=duration)
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                target_user.id,
                permissions={'can_send_messages': False},
                until_date=until_date
            )
            await update.message.reply_text(f"🔇 {target_user.mention_html()} has been muted for {context.args[1]}!", parse_mode='HTML')
        else:
            await context.bot.restrict_chat_member(
                update.effective_chat.id,
                target_user.id,
                permissions={'can_send_messages': False}
            )
            await update.message.reply_text(f"🔇 {target_user.mention_html()} has been muted!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to mute user: {str(e)}")

@admin_only
async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to unmute them.")
        return
    
    try:
        await context.bot.restrict_chat_member(
            update.effective_chat.id,
            target_user.id,
            permissions={
                'can_send_messages': True,
                'can_send_media_messages': True,
                'can_send_polls': True,
                'can_send_other_messages': True,
                'can_add_web_page_previews': True
            }
        )
        await update.message.reply_text(f"🔊 {target_user.mention_html()} has been unmuted!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to unmute user: {str(e)}")
