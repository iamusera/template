
class ResolverMessage:
    code = "1"
    message = ""

    def __init__(self, code, message) -> None:
        self.code = code
        self.message = message

    @staticmethod
    def from_message(message):
        return ResolverMessage("1", message)
