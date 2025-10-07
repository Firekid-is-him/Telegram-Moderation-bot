import json
import os

def read_json(file_path):
    if not os.path.exists(file_path):
        return {}
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except:
        return {}

def write_json(file_path, data):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)

def get_chat_data(file_path, chat_id):
    data = read_json(file_path)
    chat_id_str = str(chat_id)
    if chat_id_str not in data:
        data[chat_id_str] = {}
    return data, chat_id_str

def save_chat_data(file_path, data):
    write_json(file_path, data)
