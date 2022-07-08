# system
import os
import signal
import threading
import time
import datetime
import random
import sys
import inspect
import importlib

# core
import tasks
from tasks import task
from settings import settings as settings
from script import Script
from game import Game
from game import ToramGame

# extern
import keyboard
from pywinauto.application import Application
from pywinauto import win32defines
from ctypes import *
from PIL import Image

# utils
from util.string import string_repeat
import util.win32 as win32
import util.math as math
import util.color as color
import util.common as common

os.system('mode con: cols=100 lines=41')

sys.path.append("scripts")

main = None
game_class = ToramGame

class Main:
  def __init__(self):
    self.enabled = True
    self.settings = settings
    self.game = game_class(settings["game"])
    self.scripts = []
    self.keybinds = {}
    tasks.main = self

  def is_active(self):
    return self.game.is_active()

  def toggle(self, *args):
    self.enable(not self.enabled)

  def enable(self, enabled):
    if enabled:
      print(" Enabled"+string_repeat(' ', 20))
    else:
      print(" Disabled"+string_repeat(' ', 20))

    self.enabled = enabled
    self.game.enabled = enabled
    
    for script in self.scripts:
      script.enabled = enabled

  def quit(self, *args):
    print(" >> Quitting"+string_repeat(' ', 20))
    print()
    # a normal exit won't work if the program hangs, need to do this
    os.kill(os.getpid(), signal.SIGTERM)

  def load(self):
    self.keybinds = settings["keybinds"]
    keyboard.on_release_key(self.keybinds["pause"], main.toggle)
    keyboard.on_release_key(self.keybinds["quit"],  main.quit)

    # enable listening to keyboard and mouse events
    for action in self.keybinds:
      key = self.keybinds[action]
      print(f" press {key} to {action}")
    print()

    # Load game
    self.game.load()

    # Load scripts
    self.load_scripts()

  def start(self):
    # Start game
    self.game.start()

    # Start scripts
    self.start_scripts()

  def load_scripts(self):
    configs = self.settings.get("scripts")
    if not configs:
      return

    for name in configs:
      config = configs[name]
      module = importlib.import_module(name)
      # load script classes
      for name, obj in inspect.getmembers(module):
        if obj is Script:
          continue
        if not inspect.isclass(obj) or not issubclass(obj, Script):
          continue

        script = obj(self, config)
        script.load()
        self.scripts.append(script)
    print(f" Loaded {len(self.scripts)} script classes")
    print()

  def start_scripts(self):
    count = 0
    for script in self.scripts:
      if script.enabled:
        script.start()
        count+=1
    print()
    print(f" Started {count} scripts")
    print()


if __name__ == "__main__":
  print("")
  print(" Welcome to")
  print(" _____                   _____     _   \n|_   _|___ ___ ___ _____| __  |___| |_ \n  | | | . |  _| .\'|     | __ -| . |  _|\n  |_| |___|_| |__,|_|_|_|_____|___|_|  \n                                       ")

  main = Main()
  main.load()
  main.start()
