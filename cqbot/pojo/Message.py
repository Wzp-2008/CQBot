from typing import List
from requests import Response, post
from .User import User
from .Command import Command
from .Errors import *


def is_command(content: str) -> bool:
    """
    IS THIS MESSAGE IS A COMMAND?
    :param content: THE TEXT CONTENT OF MESSAGE
    :return: A BOOL OF THIS MESSAGE HAVE
    """
    return "/" in content


class ChannelMessage:
    """
    A Class for ChannelMessage
    """
    def __init__(self, sender: User, cid: int, gid: int, content: str):
        self.sender = sender
        self.cid = cid
        self.gid = gid
        self.content = content
        if is_command(self.content):
            self.command = Command(content)
        else:
            raise ParseCommandError("this is not a command!")

    def getCommand(self) -> Command:
        """
        get this message's command object
        :return: command object
        """
        return self.command

    def getCommandHead(self) -> str:
        """
        get this message's command head
        example: /abc 123 it will return abc
        :return: the command head
        """
        return self.command.getHead()

    def getCommandBody(self) -> List[str]:
        """
        get this message's command body
        example: /abc 123 it will return ["123"]
        :return: a list of command body
        """
        return self.command.getBody()

    def Reply(self, content: str, have_at=False) -> Response:
        """
        Reply this message
        :param content: the content you want to reply
        :param have_at: is it have an at? if it's not, this method will add it
        :return:the response from the server
        """
        if have_at:
            m = content
        else:
            m = self.sender.getAT() + content
        return post("http://192.168.123.3:20000/send_guild_channel_msg",
                    data={"guild_id": self.gid,
                          "channel_id": self.cid,
                          "message": m
                          }
                    )


class ChannelMessageWithoutCommand:
    """
    no command's ChannelMessage
    """
    def __init__(self, sender: User, cid: int, gid: int, content:str):
        self.sender = sender
        self.cid = cid
        self.gid = gid
        self.content = content

    def getContent(self) -> str:
        return self.content

    def Reply(self, content: str, have_at=False) -> Response:
        """
        Reply this message
        :param content: the content you want to reply
        :param have_at: is it have an at? if it's not, this method will add it
        :return:the response from the server
        """
        if have_at:
            m = content
        else:
            m = self.sender.getAT() + content
        return post("http://192.168.123.3:20000/send_guild_channel_msg",
                    data={"guild_id": self.gid,
                          "channel_id": self.cid,
                          "message": m
                          }
                    )
