# system
import time
import random
import json

# extern
from pywinauto.application import Application
from pywinauto import win32defines
from ctypes import *

# core
import tasks
from tasks import task

# util
import util.win32 as win32
import util.color as color

class Game(object):
  def __init__(self, config):
    self.enabled = True
    self.config = config
    self.name = config["title"]
    self.data = {}
    self.app = None
    self.window = None
    self.screen_capture = None
    #print(self.window.write_to_xml("test.xml"))

  def load(self):
    print(f" Attaching to '{self.name}' ...")
    # Attach to application
    self.app = Application(backend="win32").connect(title=self.name, timeout=10)
    self.window = self.app.window(title=self.name)

    if self.window:
      print(f" Successfully attached!")
    print()

    # Load tasks
    t = self.config.get("tasks")
    print(t)
    self.tasks = tasks.process(t, self)

  def start(self):
    print(f"Starting Game")
    for task in self.tasks:
      task.start()
      print(f"  -> Task '{task.name}'")
      print(f"     Delay: {task.delay}")

  def is_active(self):
    return self.name in win32.window_current()

  def scan(self, *args):
    self.screen_capture, result = win32.capture_screen(self.name)
    #if result:
    #  self.screen_capture.save("testing.png")
  

class ToramGame(Game):
  def __init__(self, config):
    super().__init__(config)
    self.health_chunks = [
      [686,731],
      [742,787],
      [797,841],
      [853,897],
      [909,953],
      [964,1008],
      [1020,1064],
      [1075,1120],
      [1131,1175],
      [1186,1231]
    ]

  @task(delay=0.5, silent=True)
  def scan(self, *args):
    Game.scan(self, *args)

    self.data["mana"] = self.read_mana()
    #self.data["health"] = self.read_health()
    # custom scans
    # coord = x, y = 954, 944
    # pixel = img.getpixel(coord)
    # target_rgb = [104, 234, 212]
    # if (color.is_match(pixel, target_rgb, 15)):
    #   self.window.send_keystrokes("e")

  def read_mana(self):
    if not self.is_health_showing():
      return

    y = 913
    rgbs = [[105, 237, 213], [108, 246, 95]]
    total = 0
    amount = 0

    for chunk in self.health_chunks:
      start = chunk[0]
      end = chunk[1]
      
      for x in range(start, end):
        total+=1
        for rgb in rgbs:
          pixel = self.screen_capture.getpixel((x, y))
          if (color.is_match(pixel, rgb, 20)):
            amount+=1
            break

    percent = (amount / total) * 100
    #print("amount: " + str(amount))
    #print("total: " + str(total))
    #print("percent: " + str(percent))
    return percent

  def is_health_showing(self):
    rgb = [58, 152, 65]
    pixel = self.screen_capture.getpixel((685, 875))
    return color.is_match(pixel, rgb, 0)