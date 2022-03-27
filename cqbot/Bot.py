from json import loads
from websocket import WebSocketApp
from .interface import *
from .enums import *
from requests import *


class Bot(object):
    """
    the main class of this SDK
    """
    websocket_uri: str = ""
    http_url: str = ""
    qid: int = None
    nickname: str = ""
    not_found_command_message: str = ""
    failed_run_message: str = ""
    commands: Dict[Command, CommandExecutor] = {}
    events: Dict[EventType, List[EventHandler]] = {}

    def __init__(self,
                 websocket_uri: str,
                 http_url: str,
                 not_found_command_message: str = "不正确的指令！",
                 failed_run_message: str = "指令执行失败"):
        """
        :param websocket_uri: an url of websocket service
        :param http_url: an url of http service
        :param not_found_command_message: when the command not found the bot will say a message of this
        :param failed_run_message: when the command not run well boot will say a message of this
        """
        self.failed_run_message = failed_run_message
        self.websocket_uri = websocket_uri
        if "/" not in http_url:
            self.http_url = http_url + "/"
        else:
            self.http_url = http_url
        self_data = post(http_url + "get_guild_service_profile").json()["data"]
        self.nickname = self_data["nickname"]
        self.qid = self_data["tiny_id"]
        self.not_found_command_message = not_found_command_message
        for obj in Types:
            self.events[obj] = []

    def on_message(self, c: WebSocketApp, data: str):
        """
        when the bot get a message
        it will call this function
        :param c: websocket connection
        :param data: the data send by server
        :return: no return
        """
        d = loads(data)
        if d["post_type"] == "message":
            if d["message_type"] == "guild":
                if d["sub_type"] == "channel":
                    # 频道消息处理部分
                    cid = d["channel_id"]  # 获取频道ID
                    gid = d["guild_id"]  # 获取子频道的ID
                    user = new_User(d['sender'])  # 获取消息发送者
                    message = d["message"]  # 获取消息
                    mw = ChannelMessageWithoutCommand(user, cid, gid, message)  # 创建消息对象
                    event = self.events[BotChannelGetMessageEvent]  # 获取已注册的event
                    e = EventType(BotChannelGetMessageEvent.args,
                                  BotGroupGetMessageEvent.name)  # BotChannelGetMessageEvent
                    e.set("message", mw)  # 设置参数
                    for i in event:  # 运行event
                        result = i.handler(e)
                        if not result:
                            print("执行BotChannelGetMessageEvent出现错误")
                    if f"[CQ:at,qq={self.qid}]" in message:
                        message = message.replace(f"[CQ:at,qq={self.qid}] ", "")
                        try:
                            m = ChannelMessage(user, cid, gid, message)
                        except ParseCommandError:
                            mw.Reply(self.not_found_command_message)
                            return
                        command = m.getCommand()
                        if command not in self.commands:
                            m.Reply(self.not_found_command_message)
                        else:
                            is_success = self.commands[command].execute(m)
                            if not is_success:
                                m.Reply(self.failed_run_message)
            elif d["message_type"] == "group":
                # 群消息处理部分
                pass
        elif d["post_type"] == "notice":
            notice_type = d["notice_type"]
            if notice_type == "message_reactions_updated":
                # 频道消息表情贴更新
                event = self.events[BotChannelMessageReactionsUpdatedEvent]
                d_ = d
                d_['current_reactions'] = getReactionInfo(d_['current_reactions'])
                e = getEvent(BotChannelMessageReactionsUpdatedEvent, d_)
                for i in event:
                    i.handler(e)
            elif notice_type == "channel_updated":
                # 子频道消息更新
                pass
            elif notice_type == "channel_created":
                # 子频道创建
                pass
            elif notice_type == "channel_destroyed":
                # 子频道删除
                pass

    def register_new_command(self, c: Command, e: CommandExecutor) -> bool:
        """
        this method cna register a command
        :param c: the command object you want to register
        :param e: the command's executor
        :return: a bool of result when the same command is register by other plugin,it will be False else is True
        """
        if c in self.commands:
            return False
        self.commands[c] = e
        return True

    def register_event(self, t: EventType, h: EventHandler) -> bool:
        """
        register an event handler to an event
        now is not support for your owner event
        :param t: an event type object for event you want to register
        :param h: an event handler
        :return: is successful
        """
        if t in self.events:
            self.events[t].append(h)
        else:
            return False
        return True

    @staticmethod
    def on_error(c: WebSocketApp, e):
        """
        this will call by websocket when the connection have an error
        :param c: websocket connection
        :param e: an error
        :return: no return
        """
        print("have error")
        print(e.args)
        print(type(e))

    @staticmethod
    def on_close(c: WebSocketApp):
        """
        it will call by websocket when the connection closed
        :param c: websocket connection
        :return: no return
        """
        print("Bot was closed!")

    @staticmethod
    def on_open(c: WebSocketApp):
        """
        it will call by websocket when the connection opened
        :param c: websocket connection
        :return: no return
        """
        print("Bot was start!")

    def start(self):
        """
        you can call this function to start the websocket connection
        :return: no return
        """
        ws = WebSocketApp(
            self.websocket_uri,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        ws.on_open = self.on_open
        ws.run_forever()
