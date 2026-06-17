"""あいさつのロジック（仕様1・仕様2）"""

GREETINGS = {1: "Hello, World!", 2: "こんにちは、世界！"}
DEFAULT = "Hello, World!"


class GreetingService:
    def __init__(self):
        self._history = []

    def greet(self, number: int) -> str:
        message = GREETINGS.get(number, DEFAULT)
        self._history.append(message)
        return message

    def history(self) -> list:
        return self._history
