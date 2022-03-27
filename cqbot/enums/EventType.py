from typing import Dict, Optional
from ..pojo import *


class EventType(object):
    """
    an event type enum
    """
    name: str = ""
    args: List[str] = []
    args_with_content: Optional[Dict[str, object]] = {}

    def __init__(self, args: List[str], name: str = "", args_with_content: Optional[Dict[str, object]] = None):
        self.args = args
        if args_with_content is None:
            self.args_with_content = {}
        else:
            self.args_with_content = args_with_content
        self.name = name

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

    def __eq__(self, other):
        return self.args == other.args and self.name == other.name

    def __hash__(self):
        return hash((self.args, self.name))


def getEvent(e_types: EventType, args: Dict[str, str]) -> EventType:
    event = EventType(e_types.args, e_types.name)
    for i in args.keys():
        event.set(i, args[i])
    return event


BotChannelGetMessageEvent = EventType(["message"], "BotChannelGetMessageEvent")
BotGroupGetMessageEvent = EventType(["message"], "BotGroupGetMessageEvent")
BotChannelMessageReactionsUpdatedEvent = EventType(
    ["guild_id", "channel_id", "user_id", "message_id", "current_reactions"],
    "BotChannelMessageReactionsUpdatedEvent"
)
Types = [
    BotChannelGetMessageEvent,
    BotGroupGetMessageEvent,
    BotChannelMessageReactionsUpdatedEvent,
]
