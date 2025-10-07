from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only, check_permission
from utils.storage import get_chat_data, save_chat_data, read_json, write_json
from utils.helpers import format_welcome_message, parse_time

@admin_only
async def set_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /setrules <rules text>")
        return
    
    rules_text = ' '.join(context.args)
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    data[chat_id_str]['rules'] = rules_text
    save_chat_data('data/settings.json', data)
    
    await update.message.reply_text("✅ Group rules have been set!")

@check_permission('rules')
async def show_rules(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    rules = data[chat_id_str].get('rules', 'No rules set for this group.')
    await update.message.reply_text(f"<b>Group Rules</b>\n\n{rules}", parse_mode='HTML')

@admin_only
async def set_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo_id = update.message.reply_to_message.photo[-1].file_id
        caption = update.message.reply_to_message.caption or ' '.join(context.args)
        
        data[chat_id_str]['welcome_photo'] = photo_id
        data[chat_id_str]['welcome_text'] = caption
    else:
        if not context.args:
            await update.message.reply_text("Usage: /setwelcome <text> or reply to a photo")
            return
        welcome_text = ' '.join(context.args)
        data[chat_id_str]['welcome_text'] = welcome_text
        if 'welcome_photo' in data[chat_id_str]:
            del data[chat_id_str]['welcome_photo']
    
    data[chat_id_str]['welcome_enabled'] = True
    save_chat_data('data/settings.json', data)
    await update.message.reply_text("✅ Welcome message has been set!")

@admin_only
async def toggle_welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['on', 'off']:
        await update.message.reply_text("Usage: /welcome <on|off>")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    enabled = context.args[0].lower() == 'on'
    data[chat_id_str]['welcome_enabled'] = enabled
    save_chat_data('data/settings.json', data)
    
    status = "enabled" if enabled else "disabled"
    await update.message.reply_text(f"✅ Welcome messages {status}!")

@admin_only
async def set_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    if update.message.reply_to_message and update.message.reply_to_message.photo:
        photo_id = update.message.reply_to_message.photo[-1].file_id
        caption = update.message.reply_to_message.caption or ' '.join(context.args)
        
        data[chat_id_str]['goodbye_photo'] = photo_id
        data[chat_id_str]['goodbye_text'] = caption
    else:
        if not context.args:
            await update.message.reply_text("Usage: /setgoodbye <text> or reply to a photo")
            return
        goodbye_text = ' '.join(context.args)
        data[chat_id_str]['goodbye_text'] = goodbye_text
        if 'goodbye_photo' in data[chat_id_str]:
            del data[chat_id_str]['goodbye_photo']
    
    data[chat_id_str]['goodbye_enabled'] = True
    save_chat_data('data/settings.json', data)
    await update.message.reply_text("✅ Goodbye message has been set!")

@admin_only
async def toggle_goodbye(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args or context.args[0].lower() not in ['on', 'off']:
        await update.message.reply_text("Usage: /goodbye <on|off>")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    enabled = context.args[0].lower() == 'on'
    data[chat_id_str]['goodbye_enabled'] = enabled
    save_chat_data('data/settings.json', data)
    
    status = "enabled" if enabled else "disabled"
    await update.message.reply_text(f"✅ Goodbye messages {status}!")

@admin_only
async def set_permission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /setpermission <command> <user|admin>")
        return
    
    command = context.args[0].lower()
    level = context.args[1].lower()
    
    permissions = read_json('permissions.json')
    
    if command not in permissions:
        await update.message.reply_text(f"Invalid command. Available: {', '.join(permissions.keys())}")
        return
    
    if level not in ['user', 'admin']:
        await update.message.reply_text("Level must be 'user' or 'admin'")
        return
    
    permissions[command] = level
    write_json('permissions.json', permissions)
    
    await update.message.reply_text(f"✅ Permission for /{command} set to {level}!")

@admin_only
async def set_maxwarn_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /maxwarn-action <ban|kick|tempban> [duration]")
        return
    
    action = context.args[0].lower()
    
    if action not in ['ban', 'kick', 'tempban']:
        await update.message.reply_text("Action must be: ban, kick, or tempban")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    data[chat_id_str]['maxwarn_action'] = action
    
    if action == 'tempban' and len(context.args) > 1:
        duration = parse_time(context.args[1])
        if duration:
            data[chat_id_str]['maxwarn_duration'] = duration
        else:
            await update.message.reply_text("Invalid duration format. Using default 1h.")
            data[chat_id_str]['maxwarn_duration'] = 3600
    
    save_chat_data('data/settings.json', data)
    await update.message.reply_text(f"✅ Max warn action set to {action}!")

@admin_only
async def set_blacklistword_action(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: /blacklistword-action <delete|delete+warn|delete+notify>")
        return
    
    action = context.args[0].lower()
    
    if action not in ['delete', 'delete+warn', 'delete+notify']:
        await update.message.reply_text("Action must be: delete, delete+warn, or delete+notify")
        return
    
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)
    
    data[chat_id_str]['blacklist_action'] = action
    save_chat_data('data/settings.json', data)
    
    await update.message.reply_text(f"✅ Blacklist action set to {action}!")
