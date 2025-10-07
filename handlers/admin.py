from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_only, check_permission
from utils.helpers import get_user_from_message

@admin_only
async def promote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to promote them.")
        return
    
    title = ' '.join(context.args[1:]) if len(context.args) > 1 else ""
    
    try:
        await context.bot.promote_chat_member(
            update.effective_chat.id,
            target_user.id,
            can_change_info=True,
            can_delete_messages=True,
            can_invite_users=True,
            can_restrict_members=True,
            can_pin_messages=True,
            can_promote_members=False
        )
        
        if title:
            await context.bot.set_chat_administrator_custom_title(
                update.effective_chat.id,
                target_user.id,
                title
            )
        
        await update.message.reply_text(f"⭐️ {target_user.mention_html()} has been promoted to admin!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to promote user: {str(e)}")

@admin_only
async def demote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message to demote them.")
        return
    
    try:
        await context.bot.promote_chat_member(
            update.effective_chat.id,
            target_user.id,
            can_change_info=False,
            can_delete_messages=False,
            can_invite_users=False,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False
        )
        await update.message.reply_text(f"📉 {target_user.mention_html()} has been demoted!", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to demote user: {str(e)}")

@admin_only
async def set_title(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target_user = get_user_from_message(update.message)
    
    if not target_user:
        await update.message.reply_text("Please reply to a user or mention them.")
        return
    
    if isinstance(target_user, str):
        await update.message.reply_text("Please reply to a user's message.")
        return
    
    if not context.args or len(context.args) < 2:
        await update.message.reply_text("Usage: /settitle @user <title>")
        return
    
    title = ' '.join(context.args[1:])
    
    try:
        await context.bot.set_chat_administrator_custom_title(
            update.effective_chat.id,
            target_user.id,
            title
        )
        await update.message.reply_text(f"✅ Set admin title for {target_user.mention_html()}: {title}", parse_mode='HTML')
    except Exception as e:
        await update.message.reply_text(f"Failed to set title: {str(e)}")

@check_permission('invitelink')
async def get_invite_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        link = await context.bot.export_chat_invite_link(update.effective_chat.id)
        await update.message.reply_text(f"📎 Invite Link: {link}")
    except Exception as e:
        await update.message.reply_text(f"Failed to get invite link: {str(e)}")
