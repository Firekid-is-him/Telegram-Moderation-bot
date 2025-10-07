from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ChatMemberHandler
import config
from utils.storage import read_json, get_chat_data, save_chat_data
from utils.helpers import format_welcome_message
from datetime import datetime
import requests

from handlers.start import start, help_command
from handlers.moderation import warn_user, kick_user, ban_user, unban_user, mute_user, unmute_user
from handlers.messages import delete_message, purge_messages
from handlers.locks import lock, unlock, lockall, unlockall
from handlers.admin import promote, demote, set_title, get_invite_link
from handlers.pins import pin_message, unpin_message, unpin_all
from handlers.info import get_user_info, check_warns, reset_warns
from handlers.settings import (
    set_rules, show_rules, set_welcome, toggle_welcome,
    set_goodbye, toggle_goodbye, set_permission, 
    set_maxwarn_action, set_blacklistword_action
)
from handlers.filters import (
    add_filter, list_filters, remove_filter,
    add_blacklist, remove_blacklist, show_blacklist
)

async def set_bot_description():
    """Set the bot description and bio on startup and periodically"""
    try:
        description = """Made By Firekid
For premium bot files meet at @unikruzng
For the bot files(free).
You cant add this bot to your group. 
You have to deploy your own file. Deploy it here
https://github.com/Firekid-is-him/Telegram-Moderation-bot"""

        short_description = "Made By Firekid | Premium: @unikruzng | Deploy here Free: github.com/Firekid-is-him/Telegram-Moderation-bot"

        url_desc = f"https://api.telegram.org/bot{config.BOT_TOKEN}/setMyDescription"
        data_desc = {"description": description}
        response_desc = requests.post(url_desc, json=data_desc)
        result_desc = response_desc.json()

        url_short = f"https://api.telegram.org/bot{config.BOT_TOKEN}/setMyShortDescription"
        data_short = {"short_description": short_description}
        response_short = requests.post(url_short, json=data_short)
        result_short = response_short.json()

        if result_desc.get('ok') and result_short.get('ok'):
            print("✓ Bot description and bio updated successfully!")
        else:
            if not result_desc.get('ok'):
                print(f"✗ Failed to update bot description: {result_desc.get('description', 'Unknown error')}")
            if not result_short.get('ok'):
                print(f"✗ Failed to update bot bio: {result_short.get('description', 'Unknown error')}")
    except Exception as e:
        print(f"✗ Error setting bot description: {e}")

async def handle_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner_in_group(update, context):
        return

    for member in update.message.new_chat_members:
        chat_id = update.effective_chat.id
        data, chat_id_str = get_chat_data('data/settings.json', chat_id)

        if not data[chat_id_str].get('welcome_enabled', False):
            continue

        welcome_text = data[chat_id_str].get('welcome_text', '')
        welcome_photo = data[chat_id_str].get('welcome_photo')

        if welcome_text:
            welcome_text = format_welcome_message(welcome_text, member, update.effective_chat)

        try:
            if welcome_photo:
                await context.bot.send_photo(
                    chat_id,
                    welcome_photo,
                    caption=welcome_text,
                    parse_mode='HTML'
                )
            elif welcome_text:
                await update.message.reply_text(welcome_text, parse_mode='HTML')
        except Exception as e:
            print(f"Error sending welcome message: {e}")

async def handle_left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await check_owner_in_group(update, context):
        return

    member = update.message.left_chat_member
    chat_id = update.effective_chat.id
    data, chat_id_str = get_chat_data('data/settings.json', chat_id)

    if not data[chat_id_str].get('goodbye_enabled', False):
        return

    goodbye_text = data[chat_id_str].get('goodbye_text', '')
    goodbye_photo = data[chat_id_str].get('goodbye_photo')

    if goodbye_text:
        goodbye_text = format_welcome_message(goodbye_text, member, update.effective_chat)

    try:
        if goodbye_photo:
            await context.bot.send_photo(
                chat_id,
                goodbye_photo,
                caption=goodbye_text,
                parse_mode='HTML'
            )
        elif goodbye_text:
            await update.message.reply_text(goodbye_text, parse_mode='HTML')
    except Exception as e:
        print(f"Error sending goodbye message: {e}")

async def check_owner_in_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check if bot owner is in the group as admin or creator"""
    if update.effective_chat.type == 'private':
        return True

    try:
        owner_member = await update.effective_chat.get_member(config.OWNER_ID)
        if owner_member.status not in ['creator', 'administrator']:
            try:
                await update.effective_chat.leave()
            except:
                pass
            return False
    except Exception:
        try:
            await update.effective_chat.leave()
        except:
            pass
        return False

    return True

async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    if not await check_owner_in_group(update, context):
        return

    chat_id = update.effective_chat.id
    user = update.effective_user

    member = await update.effective_chat.get_member(user.id)
    is_admin = member.status in ['creator', 'administrator']

    locks_data, locks_chat_id = get_chat_data('data/locks.json', chat_id)
    locks = locks_data[locks_chat_id].get('locks', [])

    if not is_admin:
        if update.message.text and 'messages' in locks:
            try:
                await update.message.delete()
                return
            except:
                pass

        if 'media' in locks:
            if (update.message.photo or update.message.video or 
                update.message.document or update.message.audio or 
                update.message.voice or update.message.video_note):
                try:
                    await update.message.delete()
                    return
                except:
                    pass

        if update.message.sticker and 'stickers' in locks:
            try:
                await update.message.delete()
                return
            except:
                pass

        if update.message.entities and 'links' in locks:
            for entity in update.message.entities:
                if entity.type in ['url', 'text_link']:
                    try:
                        await update.message.delete()
                        return
                    except:
                        pass

        if update.message.poll and 'polls' in locks:
            try:
                await update.message.delete()
                return
            except:
                pass

        if update.message.forward_date and 'forwards' in locks:
            try:
                await update.message.delete()
                return
            except:
                pass

    if not update.message.text:
        return

    message_text = update.message.text.lower()

    blacklist_data, blacklist_chat_id = get_chat_data('data/blacklist.json', chat_id)
    blacklisted_words = blacklist_data[blacklist_chat_id].get('words', [])

    if not is_admin and blacklisted_words:
        for word in blacklisted_words:
            if word in message_text:
                settings_data, settings_chat_id = get_chat_data('data/settings.json', chat_id)
                action = settings_data[settings_chat_id].get('blacklist_action', 'delete')

                try:
                    await update.message.delete()

                    if action == 'delete+warn':
                        warn_data, warn_chat_id = get_chat_data('data/warnings.json', chat_id)
                        user_id_str = str(user.id)

                        if user_id_str not in warn_data[warn_chat_id]:
                            warn_data[warn_chat_id][user_id_str] = []

                        warn_info = {
                            'reason': 'Used blacklisted word',
                            'time': datetime.now().isoformat()
                        }
                        warn_data[warn_chat_id][user_id_str].append(warn_info)
                        save_chat_data('data/warnings.json', warn_data)

                        msg = await context.bot.send_message(
                            chat_id,
                            f"⚠️ {user.mention_html()} warned for using blacklisted word!",
                            parse_mode='HTML'
                        )
                    elif action == 'delete+notify':
                        msg = await context.bot.send_message(
                            chat_id,
                            f"❌ {user.mention_html()} message deleted (blacklisted word)",
                            parse_mode='HTML'
                        )

                    return
                except Exception as e:
                    print(f"Error handling blacklist: {e}")

    filters_data, filters_chat_id = get_chat_data('data/filters.json', chat_id)
    custom_filters = filters_data[filters_chat_id].get('filters', {})

    for keyword, response in custom_filters.items():
        if keyword in message_text:
            try:
                await update.message.reply_text(response)
            except Exception as e:
                print(f"Error sending filter response: {e}")

async def post_init(application: Application):
    """Run after bot initialization"""
    await set_bot_description()

    application.job_queue.run_repeating(
        callback=lambda context: set_bot_description(),
        interval=600,
        first=600,
        name="update_bot_description"
    )

def main():
    print("Starting Telegram Moderation Bot...")

    app = Application.builder().token(config.BOT_TOKEN).post_init(post_init).build()

    app.bot_data['max_warns'] = config.MAX_WARNS

    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('help', help_command))

    app.add_handler(CommandHandler('warn', warn_user))
    app.add_handler(CommandHandler('kick', kick_user))
    app.add_handler(CommandHandler('ban', ban_user))
    app.add_handler(CommandHandler('unban', unban_user))
    app.add_handler(CommandHandler('mute', mute_user))
    app.add_handler(CommandHandler('unmute', unmute_user))

    app.add_handler(CommandHandler('delete', delete_message))
    app.add_handler(CommandHandler('purge', purge_messages))

    app.add_handler(CommandHandler('lock', lock))
    app.add_handler(CommandHandler('unlock', unlock))
    app.add_handler(CommandHandler('lockall', lockall))
    app.add_handler(CommandHandler('unlockall', unlockall))

    app.add_handler(CommandHandler('promote', promote))
    app.add_handler(CommandHandler('demote', demote))
    app.add_handler(CommandHandler('settitle', set_title))
    app.add_handler(CommandHandler('invitelink', get_invite_link))

    app.add_handler(CommandHandler('pin', pin_message))
    app.add_handler(CommandHandler('unpin', unpin_message))
    app.add_handler(CommandHandler('unpinall', unpin_all))

    app.add_handler(CommandHandler('info', get_user_info))
    app.add_handler(CommandHandler('warns', check_warns))
    app.add_handler(CommandHandler('resetwarns', reset_warns))

    app.add_handler(CommandHandler('setrules', set_rules))
    app.add_handler(CommandHandler('rules', show_rules))
    app.add_handler(CommandHandler('setwelcome', set_welcome))
    app.add_handler(CommandHandler('welcome', toggle_welcome))
    app.add_handler(CommandHandler('setgoodbye', set_goodbye))
    app.add_handler(CommandHandler('goodbye', toggle_goodbye))
    app.add_handler(CommandHandler('setpermission', set_permission))
    app.add_handler(CommandHandler('maxwarnaction', set_maxwarn_action))
    app.add_handler(CommandHandler('blacklistwordaction', set_blacklistword_action))

    app.add_handler(CommandHandler('filter', add_filter))
    app.add_handler(CommandHandler('filters', list_filters))
    app.add_handler(CommandHandler('stop', remove_filter))
    app.add_handler(CommandHandler('blacklist', add_blacklist))
    app.add_handler(CommandHandler('unblacklist', remove_blacklist))
    app.add_handler(CommandHandler('blacklisted', show_blacklist))

    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, handle_new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, handle_left_member))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    app.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.Document.ALL | filters.AUDIO | 
        filters.VOICE | filters.VIDEO_NOTE | filters.Sticker.ALL | 
        filters.FORWARDED | filters.POLL, 
        handle_messages
    ))

    print("Bot is running! Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
