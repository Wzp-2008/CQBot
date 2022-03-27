class User:
    """
    A class for user
    """
    def __init__(self, nickname: str, user_id: int):
        self.nickname = nickname
        self.user_id = user_id

    def getAT(self) -> str:
        """
        get the cq code of at sb
        :return: a string with cq code
        """
        return f"[CQ:at,qq={self.user_id}] "


def new_User(dictionary: dict) -> User:
    """
    get a user from data's sender
    :param dictionary: sender
    :return: a user object
    """
    return User(dictionary['nickname'], dictionary['user_id'])
