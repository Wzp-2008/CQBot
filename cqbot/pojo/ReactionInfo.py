from typing import Dict


class ReactionInfo(object):
    emoji_id: str = ""
    emoji_index: int = 0
    emoji_type: int = 0
    emoji_name: str = ""
    count: int = 0
    clicked: bool = False

    def __init__(self,
                 emoji_id: str,
                 emoji_index: int,
                 emoji_type: int,
                 emoji_name: str,
                 count: int,
                 clicked: bool):
        self.emoji_id = emoji_id
        self.emoji_index = emoji_index
        self.emoji_type = emoji_type
        self.emoji_name = emoji_name
        self.count = count
        self.clicked = clicked


def getReactionInfo(d: Dict) -> ReactionInfo:
    return ReactionInfo(d['emoji_id'], d['emoji_index'], d['emoji_type'], d['emoji_name'], d['count'], d['clicked'])
