#!/usr/bin/python                                                                                                       
## Selected window: https://gist.github.com/luckman212/91cdd9a08e98a9f01214bdfde3057e85
# references
#  https://developer.apple.com/documentation/appkit/nsworkspace
#  https://bmn.name/post/2016/05/28/current-osx-app/
#  https://stackoverflow.com/questions/28815863/how-to-get-active-window-title-using-python-in-mac
#  https://apple.stackexchange.com/questions/123730/is-there-a-way-to-detect-what-program-is-stealing-focus-on-my-mac/

try:
	from AppKit import NSWorkspace
except ImportError:
	print("No import")
	exit(1)

from datetime import datetime
from time import sleep
from time import time
import os
from DiscordRPC import RPC
import threading
import AppKit


last_active_name = ""
active = True
CLOSE_DISCORD = True
DISCORD_RPC = True
IDLE = True
IDE = ["Code", "Intellij", "Jetbrains"]
def threadSelectedProcess():
    global Discord, active, last_active_name
    active = True
    while active:
        active_app = NSWorkspace.sharedWorkspace().activeApplication()
        if active_app:
            if active_app['NSApplicationName'] != last_active_name:
                last_active_name = active_app['NSApplicationName']
                if last_active_name == "Discord":
                    if CLOSE_DISCORD:
                        active_app.hide()
                    
                elif DISCORD_RPC:
                    if last_active_name == "OneNote":
                        Discord.setSituation("Taking notes")
                    elif IDE.__contains__(last_active_name):
                        Discord.setSituation("Coding")
                    elif last_active_name == "Safari":
                        Discord.setSituation("Watching lectures")
                    elif last_active_name == "Anteprima":
                        Discord.setSituation("Reading notes")
                        
                    else:
                        Discord.setSituation("On this application: " + last_active_name)
                
def processExists(name="OneNote") -> bool:
    for process in os.popen('ps aux'):
        if process.__contains__(name):
            return True
    return False

def getMouseCoordinates():
    pos = AppKit.NSEvent.mouseLocation()
    return [pos.x, pos.y]

def isIdling(mouseCoords):
    idleTIME = 60*15
    timeNow = time()
    nowMouseCoords = getMouseCoordinates()
    if nowMouseCoords[0] == mouseCoords[0] and nowMouseCoords[1] == mouseCoords[1]:
        return timeNow - mouseCoords[2] >= idleTIME, mouseCoords
    else:
        return False, [nowMouseCoords[0], nowMouseCoords[1], timeNow]

def main():
    global Discord, active
    existedBefore = False
    mouseCoords = [-5000, -5000, 0]
    while True:
        if processExists:
            if not existedBefore:
                if DISCORD_RPC:
                    Discord.start()
                existedBefore = True
                threading.Thread(target=threadSelectedProcess).start()
            else:
                if IDLE:
                    idling, mouseCoords = isIdling(mouseCoords)
                    if idling:
                        Discord.setSituation("Idling")
        else:
             if existedBefore:
                if DISCORD_RPC:
                    RPC.stop()
                existedBefore = False
                active = False
        sleep(10)
            

if __name__ == "__main__":
    global Discord
    if DISCORD_RPC:
        Discord = RPC()
    main()

	