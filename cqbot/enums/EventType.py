from typing import Dict, Optional
from ..pojo import *


class EventType(object):
    """
    an event type enum
    """
    args: List[str] = []
    args_with_content: Optional[Dict[str, object]] = {}

    def __init__(self, args: List[str], args_with_content: Optional[Dict[str, object]] = None):
        self.args = args
        if args_with_content is None:
            self.args_with_content = {}
        else:
            self.args_with_content = args_with_content

    def get(self, key: str) -> Optional[object]:
        """
        get args from the event
        :param key: the key you wanted
        :return: no return
        """
        try:
            return self.args_with_content[key]
        except KeyError:
            return None

    def set(self, key: str, value: object):
        """
        set args from the event
        :param key: the key
        :param value: the value
        :return: no return
        """
        self.args_with_content[key] = value


BotChannelGetMessageEvent = EventType(["message"])
BotGroupGetMessageEvent = EventType(["message"])
