'''
    Author: TechAle (alessandro.condello.email@gmail.com)
    Since: 14/03/23
    Description: Tracks every activity you are doing on your Mac
'''
from managers.ProcessManager import processManager

if __name__ == "__main__":
    manager = processManager()
    manager.loadConfiguration()
    manager.start()