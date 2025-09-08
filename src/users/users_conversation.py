"""Module management for API communication regarding users
    """

import httpx
from src.database.class_connection_manager import get_connection_manager
from src.globals.help_functions import clear_screen
from src.menu_functions import show_menu
from .class_user import User
from .class_user_manager import get_user_manager


user_manager = get_user_manager()
connection_manager = get_connection_manager()


class Conversation:
    def __init__(self, user: User, peer_guid: str, api_addr_port: tuple[str, int] = None):
        self.user = user
        self.user_guid = user_manager.get_user_guid(user.id)
        self.peer_guid = peer_guid
        if api_addr_port is None:
            self.api_addr, self.api_port = connection_manager.get_api_address()
        else:
            self.api_addr, self.api_port = api_addr_port

        self.history = []

    @property
    def api_url(self):
        return f"http://{self.api_addr}:{self.api_port}"

    def check_required(self):
        if not all([self.peer_guid, self.user_guid, self.api_addr, self.api_port]):
            print("Not sufficient data to establish connection.")
            return False
        else:
            return True

    def get_history(self) -> list:
        result = []

        resp = httpx.get(f"{self.api_url}/get-conv", params={
            "user_guid": self.user_guid,
            "peer_guid": self.peer_guid,
            "rec_limit": 10,
            "not_received": False
        })
        for line in resp.json():
            result.append(f'{line["nickname"]}: {line["text"]}')
        # print("Conversation:", resp.json())

        return result

    def send_message(self, message: str):
        resp = httpx.post(f"{self.api_url}/send-msg", params={
            "user_guid": self.user_guid,
            "peer_guid": self.peer_guid,
            "message_text": message
        })

        if resp.json() != message:
            print("Send response:", resp.json())

    def start(self):
        """Initializing and main conversation loop"""
        if not self.check_required():
            return

        # clear_screen()
        # self.history = self.get_history()
        # for line in self.history:
        #     print(line)

        while True:
            clear_screen()
            self.history = self.get_history()
            for line in self.history:
                print(line)

            print("-q Quit | -r Refresh")
            user_input = input(f"{self.user.login}: ")

            if user_input == "-q":
                break
            elif user_input == "-r":
                clear_screen()
                self.history = self.get_history()
                for line in self.history:
                    print(line)
            else:
                self.send_result = self.send_message(user_input)

        self.stop()

    def stop(self):
        clear_screen()
