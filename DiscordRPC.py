import time

import pypresence
from pypresence import Presence
import threading
import sys
import pyautogui


class RPC:
    def __init__(self):
        self.on = True
        self.client_id = "1084765396344782868"
        self.situation = "Writing" # Reading/Writing notes, Watching lectures
        try:
            self.RPC = Presence(self.client_id)
        except pypresence.exceptions.DiscordNotFound:
            sys.exit(-1)

    def start(self):
        self.start = int(time.time())
        self.RPC.connect()
        threading.Thread(target=self.run).start()

    def stop(self):
        self.on = False

    def setSituation(self, situation):
        self.situation = situation

    def run(self):
        while self.on:
            self.RPC.update(
                large_image="pic",
                large_text="Studying",
                details=self.situation,
                start=self.start,
                buttons=[{"label": "Github", "url": "https://github.com/TechAle/"}]
            )
            time.sleep(10)