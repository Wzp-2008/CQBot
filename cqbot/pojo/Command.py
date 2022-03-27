from typing import List


class Command:
    """
    the class of command
    """
    def __init__(self, content: str):
        self.content = content
        if " " in self.content:
            self.csv = self.content.split(" ")
            self.head = self.csv[0].replace("/", "")
            self.body = self.csv[1:len(self.csv)]
        else:
            self.csv = [self.content]
            self.head = self.content.replace("/", "")
            self.body = []

    def getHead(self) -> str:
        """
        get the command head
        :return: command head
        """
        return self.head

    def getBody(self) -> List[str]:
        """
        get the command body
        :return: command body
        """
        return self.body

    def __eq__(self, other) -> bool:
        return self.head == other.head

    def __hash__(self) -> int:
        return hash(self.head)


def getCommand(head: str) -> Command:
    """
    get a command object from string you wanted
    :param head: a string of command's name(after the /)
    :return: a command object
    """
    return Command("/" + head)
