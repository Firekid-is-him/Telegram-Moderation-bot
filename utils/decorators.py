from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes
from utils.storage import read_json

def admin_only(func):
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        chat = update.effective_chat
        
        if chat.type == 'private':
            await update.message.reply_text("This command only works in groups.")
            return
        
        member = await chat.get_member(user.id)
        if member.status not in ['creator', 'administrator']:
            await update.message.reply_text("You need to be an admin to use this command.")
            return
        
        return await func(update, context)
    return wrapper

def check_permission(command_name):
    def decorator(func):
        @wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
            user = update.effective_user
            chat = update.effective_chat
            
            if chat.type == 'private':
                await update.message.reply_text("This command only works in groups.")
                return
            
            permissions = read_json('permissions.json')
            permission_level = permissions.get(command_name, 'admin')
            
            if permission_level == 'admin':
                member = await chat.get_member(user.id)
                if member.status not in ['creator', 'administrator']:
                    await update.message.reply_text("You need to be an admin to use this command.")
                    return
            
            return await func(update, context)
        return wrapper
    return decorator
