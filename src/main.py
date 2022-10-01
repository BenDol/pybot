# system
import os
import signal
import sys
import inspect
import importlib

# core
import tasks
import components
import config
from settings import settings as settings
from script import Script
from game import RunescapeGame

# extern
import keyboard

# utils
import util.string as string

os.system('mode con: cols=100 lines=41')

sys.path.append("scripts")

main = None
game_class = RunescapeGame

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

  def enable(self, enabled):
    if enabled:
      print(" Enabled" + string.repeat(' ', 20))
    else:
      print(" Disabled" + string.repeat(' ', 20))

    self.enabled = enabled
    self.game.enabled = enabled

    for script in self.scripts:
      script.enabled = enabled

  def toggle(self, *args):
    self.enable(not self.enabled)

  def quit(self, *args):
    print(" >> Quitting" + string.repeat(' ', 20))
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

    # load components
    components.load()

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
      conf = configs[name]
      module = importlib.import_module(name)
      # load script classes
      for n, obj in inspect.getmembers(module):
        if obj is Script or not inspect.isclass(obj) or not issubclass(obj, Script):
          continue

        script = obj(self, config.load("scripts/" + name))
        script.load(conf)
        self.scripts.append(script)
    print(f" Loaded {len(self.scripts)} script classes")
    print()

  def start_scripts(self):
    count = 0
    for script in self.scripts:
      if script.enabled:
        script.start()
        count += 1
    print()
    print(f" Started {count} scripts")
    print()


if __name__ == "__main__":
  print("")
  print(" Welcome to")
  print("  _______  __   __  _______  _______  _______ \n |       ||  | |  ||  _    ||       ||       |\n |    _  ||  |_|  || |_|   ||   _   ||_     _|\n |   |_| ||       ||       ||  | |  |  |   |  \n |    ___||_     _||  _   | |  |_|  |  |   |  \n |   |      |   |  | |_|   ||       |  |   |  \n |___|      |___|  |_______||_______|  |___|  \n  \n                                       ")

  main = Main()
  main.load()
  main.start()
