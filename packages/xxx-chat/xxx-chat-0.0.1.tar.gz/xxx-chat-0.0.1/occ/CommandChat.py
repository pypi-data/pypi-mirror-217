
import json
from commons.config import get_env
import os
import http.client

from utils.CommonUtil import waiting_start, waiting_stop


def get_home_path():
    homedir = os.environ.get('HOME', None)
    if os.name == 'nt':
        homedir = os.path.expanduser('~')
    return homedir

class CommandChat:

    DEFAULT_PROFILE = "default"
    DEFAULT_CHAT_LOG_ID = "chat-1"

    def __init__(self, profile=None, chat_log_id=None):
        self.api_key = get_env(profile or self.DEFAULT_PROFILE, "api_key")
        self.limit_history = int(get_env(profile or self.DEFAULT_PROFILE, "limit_history") or 4)
        self.chat_log_id = chat_log_id or self.DEFAULT_CHAT_LOG_ID
        self.folder_path = os.path.join(get_home_path(), ".xxx", profile or self.DEFAULT_PROFILE)
        self.file_name = os.path.join(self.folder_path, f"{self.chat_log_id}.log")
        os.makedirs(self.folder_path, exist_ok=True)
        if not os.path.exists(self.file_name):
            open(self.file_name, 'w').close()
        self.messages = [json.loads(line) for line in (line.strip() for line in open(self.file_name)) if line.strip()]

    def chat(self, message):
        message = {"role": "user", "content": message}
        self.messages.append(message)
        waiting_start()
        
        conn = http.client.HTTPSConnection("3gxj2qqbul.execute-api.ap-southeast-1.amazonaws.com")
        payload = ''
        headers = {
            'x-api-key': self.api_key,
            'x-message': json.dumps(message)
        }
        conn.request("GET", "/default/gateway", payload, headers)
        res = conn.getresponse()
        data = res.read().decode('unicode_escape')
        output_data = data[1:-1]

        waiting_stop()   
        print(output_data)
        print("\n")
        self.record_chat_logs(message, {"role": "assistant", "content": output_data})

    def record_chat_logs(self, content, completion_text):
        with open(self.file_name, 'r+') as f:
            lines = f.readlines()
            if len(lines) >= self.limit_history:
                with open(os.path.join(self.folder_path, self.chat_log_id + '_history.log'), 'a+') as hf:
                    hf.writelines(lines[:(self.limit_history)])
                lines = lines[(self.limit_history):]
            lines.append('\n{}\n{}'.format(json.dumps(content, ensure_ascii=False), json.dumps(completion_text, ensure_ascii=False)))
            f.seek(0)
            f.truncate()
            f.writelines(lines)


if __name__ == '__main__':
    conn = http.client.HTTPSConnection("3gxj2qqbul.execute-api.ap-southeast-1.amazonaws.com")
    payload = ''
    headers = {
    'x-api-key': 'inlDSY1cPZ9eE60Vj72Hz5b0MCfXGvFAajZTVrtS'
    }
    conn.request("GET", "/default/gateway", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))

