import re

def parse_time(time_str):
    if not time_str:
        return None
    
    match = re.match(r'(\d+)([smhd])', time_str.lower())
    if not match:
        return None
    
    amount = int(match.group(1))
    unit = match.group(2)
    
    if unit == 's':
        return amount
    elif unit == 'm':
        return amount * 60
    elif unit == 'h':
        return amount * 3600
    elif unit == 'd':
        return amount * 86400
    
    return None

def format_welcome_message(text, user, chat):
    if not text:
        return text
    
    text = text.replace('{user}', user.mention_html())
    text = text.replace('{group}', chat.title)
    text = text.replace('{id}', str(user.id))
    
    return text

def get_user_from_message(message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    
    if message.entities:
        for entity in message.entities:
            if entity.type == 'text_mention':
                return entity.user
    
    text_parts = message.text.split(maxsplit=2)
    if len(text_parts) > 1:
        username = text_parts[1].lstrip('@')
        return username
    
    return None
