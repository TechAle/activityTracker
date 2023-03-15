import threading
from signal import signal, SIGTERM, SIGINT
from time import sleep, time
from managers.DiscordManager import RPCmanager
import os
import json
try:
    from AppKit import NSApplication, NSApp, NSWorkspace
    from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo
except ImportError:
    print("AppKit is not here")
    exit(1)




class processManager:

    # Just init variables
    def __init__(self):
        self.threadDiscord = None
        self.managerAlive = True
        self.existedBefore = False
        self.processExists = False
        self.isIdling = False
        self.lastActitityTime = time()
        self.activities = {}
        self.last_active_name = ""
        signal(SIGTERM, self._onAbort)
        signal(SIGINT, self._onAbort)

    # Given a name, checks if there is a process with that name
    @staticmethod
    def processExists(name="OneNote.app") -> bool:
        for process in os.popen('ps aux'):
            if process.__contains__(name):
                return True
        return False

    # This basically manage everything
    def start(self):
        while True:
            # If the process exists
            if processManager.processExists():
                # If it hasnt existed before, then we have to start it
                if not self.existedBefore:
                    if self.configuration["DiscordRPC"]:
                        self.threadDiscord.start()
                    self.existedBefore = True
                else:
                    # Update the selected window
                    self._checkSelectedWindow()
                    # And if we are idling
                    self._checkIdling()

            else:
                # If the process doesnt exists, update things
                if self.existedBefore:
                    if self.configuration["DiscordRPC"]:
                        self.threadDiscord.stop()
                    self.existedBefore = False

    def _checkIdling(self):
        pass

    def _checkSelectedWindow(self):
        workspace = NSWorkspace.sharedWorkspace()
        active_app = workspace.activeApplication()
        # If the window is the same, just go away
        if active_app["NSApplicationName"] == self.last_active_name:
            return
        # Update informations
        self.last_active_name = active_app['NSApplicationName']
        self.lastActitityTime = time()
        if self.configuration["DiscordRPC"]:
            if self.last_active_name == "OneNote":
                self.threadDiscord.setSituation("Taking notes")
            elif self.last_active_name == "Safari":
                self.threadDiscord.setSituation("Watching lectures")
            elif self.last_active_name == "Anteprima":
                self.threadDiscord.setSituation("Reading notes")
            else:
                self.threadDiscord.setSituation("On this application: " + self.last_active_name)
        # If we are on discord, and i dont want to open discord, then close it
        if self.last_active_name != "Discord" or not self.configuration["Close_Discord"]:
            return

        '''
            Here there is a lot to explain, so, apple api are kinda shit.
            Said this, we need to get the application with name "Discord", but there is a problem
            The function runningApplications gives us a list of application, but without a name; just a pid
            If we want to identify discord, we need to iter for every active window, find the one with the same
            pid, and then we can hide it.
        '''
        activeApps = workspace.runningApplications()
        options = kCGWindowListOptionOnScreenOnly
        windowList = CGWindowListCopyWindowInfo(options,
                                                kCGNullWindowID,)
        for app in activeApps:
            for window in windowList:
                if  app.processIdentifier() == window["kCGWindowOwnerPID"]and\
                    window['kCGWindowOwnerName'] == active_app["NSApplicationName"]: 
                    # Inside if
                    app.hide()
                    break
                    
    def _onAbort(self, *args):
        self.managerAlive = False
        self.saveConfiguration()

    def _calculateActivities(self):
        for activity in self.activitiesConfiguration["Time"]:
            self._addActivity(activity, self.activitiesConfiguration["Time"][activity])

    def _addActivity(self, activity, time):
        if not self.activities.__contains__(activity):
            self.activities[activity] = 0
        self.activities[activity] += time

    def loadConfiguration(self):
        self.configuration = json.load(open("configuration.json", "r"))
        self.activitiesConfiguration = json.load(open("activities.json", "r"))
        self.activities = list(json.load(open("activities.json", "r")).keys())
        self.activities.pop(self.activities.index("Time"))
        self.activities = {k:0 for k in self.activities}
        self._calculateActivities()
        self._importLibrearies()

    def _importLibrearies(self):
        if self.configuration["DiscordRPC"]:
            self.threadDiscord = RPCmanager(threading.currentThread())

    def saveConfiguration(self):
        pass