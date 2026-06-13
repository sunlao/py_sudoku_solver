from shared.models.messages import Message
from actors.static_data.read import Read


class Startup:

    def __init__(self) -> None:
        pass
    
    def _set_process(self) -> None:
        pass

    def _send_start_game(self) -> None:
        pass

    def _send_start_rbc(self) -> None:
        pass

    def _set_rbc_status(self) -> None:
        pass

    def _send_observer(self) -> None:
        pass

    def director(self, message: Message) -> None:
        print(message.content)
