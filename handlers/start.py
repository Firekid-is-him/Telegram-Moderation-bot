from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
    Welcome To the Firekid Moderation bot, built by Firekid

    I help manage groups with powerful moderation tools.
    Use /help to see all available commands.

    For premium Files with customizable commands + able to set bot description, send me a text: https://t.me/unikruzng
    """
        await update.message.reply_text(welcome_text)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
    <b>Moderation Commands (Reply the user message) (Admin)</b>
    /warn - Warn a user 
    /kick - Remove user from group
    /ban - Ban user permanently
    /unban - Unban a user
    /mute - Mute a user
    /unmute - Unmute a user

    <b>Message Commands (Admin)</b>
    /delete - Delete replied message
    /purge - Delete last X messages

    <b>Lock Commands (Admin)</b>
    /lock - Lock message types
    Usage: /lock &lt;type&gt;
    Available types: messages, media, stickers, links, polls, forwards
    /unlock - Unlock message types
    /lockall - Lock everything
    /unlockall - Unlock everything

    <b>Admin Commands</b>
    /promote - Promote to admin
    /demote - Remove admin rights
    /settitle - Set admin title
    Usage: /settitle @user &lt;title&gt; (reply and tag the user)
    /invitelink - Get invite link

    <b>Pin Commands (Admin)</b>
    /pin - Pin a message
    /unpin - Unpin message
    /unpinall - Unpin all

    <b>Info Commands</b>
    /info - User information
    /warns - Check warnings
    /resetwarns - Clear warnings (Admin)

    <b>Settings (Admin)</b>
    /setrules - Set group rules
    /rules - Show rules
    /setwelcome - Set welcome message
    Add {user} to tag the user and {id} to add the id
    /welcome - Toggle welcome on/off
    /setgoodbye - Set goodbye message
    Add {user} to tag the user and {id} to add the id
    /goodbye - Toggle goodbye on/off

    <b>Filter Commands</b>
    /filter - Add auto-reply (Admin)
    Usage: /filter &lt;keyword&gt; &lt;response&gt;
    /filters - List filters
    /stop - Remove filter (Admin)
    Usage: /stop &lt;keyword&gt;
    /blacklist - Add blacklisted words (Admin)
    Usage: /blacklist &lt;word1&gt; &lt;word2&gt;
    /unblacklist - Remove blacklist (Admin)
    /blacklisted - Show blacklisted words

    <b>Configuration (Admin)</b>
    /setpermission - Change command permissions
    /maxwarnaction - Set max warn action
    /blacklistwordaction - Set blacklist action
    Action must be: delete, delete+warn, or delete+notify
    """
        await update.message.reply_text(help_text, parse_mode='HTML')