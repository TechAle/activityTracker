import time

import pypresence
from pypresence import Presence
import threading
import sys


class RPCmanager:
    def __init__(self, mainThread):
        self.on = True
        self.client_id = "1084765396344782868"
        self.situation = "Writing" # Reading/Writing notes, Watching lectures
        self.mainThread = mainThread
        self.hasStarted = False
        self.initPresence()


    def initPresence(self):
        try:
            self.RPC = Presence(self.client_id)
            self.hasStarted = True
        except pypresence.exceptions.DiscordNotFound:
            pass

    def start(self):
        if self.hasStarted:
            self.startTime = int(time.time())
            self.on = True
            self.RPC.connect()
            threading.Thread(target=self.run).start()


    def stop(self):
        if self.hasStarted:
            self.on = False

    def setSituation(self, situation):
        if not self.hasStarted:
            self.initPresence()
        self.situation = situation

    def run(self):
        while self.on:
            self.RPC.update(
                large_image="pic",
                large_text="Studying",
                details=self.situation,
                start=self.startTime,
                buttons=[{"label": "Github", "url": "https://github.com/TechAle/"}]
            )
            time.sleep(10)
        self.RPC.close()