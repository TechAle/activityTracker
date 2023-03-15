from AppKit import NSApplication, NSApp, NSWorkspace
from Quartz import kCGWindowListOptionOnScreenOnly, kCGNullWindowID, CGWindowListCopyWindowInfo

while True:
    workspace = NSWorkspace.sharedWorkspace()
    active_app = workspace.activeApplication()
    activeApps = workspace.runningApplications()
    for app in activeApps:
        if app.isActive():
            options = kCGWindowListOptionOnScreenOnly
            windowList = CGWindowListCopyWindowInfo(options,
                                                    kCGNullWindowID)
            for window in windowList:
                if window['kCGWindowOwnerName'] == active_app["NSApplicationName"]:
                    print(active_app["NSApplicationName"])
                    break
            break