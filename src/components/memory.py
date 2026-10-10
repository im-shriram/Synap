import json
import pathlib

from langchain_core.messages import messages_to_dict, messages_from_dict, BaseMessage
from langchain_core.load import dumps

class ChatHistory:
    def __init__(self):
        self.previous_chat_history: list[BaseMessage] | None = None
        self.current_chat_history: list[BaseMessage] | None = None

    def load_chat_history(self, path: pathlib.Path) -> list[BaseMessage]:
        try:
            with open(file=path, mode="r") as fp:
                self.previous_chat_history = messages_from_dict(json.load(fp))[1:]
        except Exception as e:
            print("No previous chats found, starting new conversation.")
            self.previous_chat_history = []

        return self.previous_chat_history
    
    def save_chat_history(self, chat_history: list[BaseMessage], path: pathlib.Path):
        with open(file=path, mode="w") as fp:
            json_chat_history_obj: str = dumps(messages_to_dict(chat_history)) # converting to list[dicts] because "BaseMessage" are not json serialization 
            fp.write(json_chat_history_obj)