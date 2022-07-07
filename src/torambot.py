import os
import signal
import threading
import time
import datetime
import random
import sys

import keyboard
from pywinauto.application import Application
from pywinauto import win32defines
from functools import wraps
from ctypes import *
from PIL import Image

from util.win32 import window_current
from util.string import string_repeat

from settings import settings as settings

os.system('mode con: cols=100 lines=41')

main = None
task_classes = {}
timers = {}

float_format = "{0:.2f}"

class task_timer(threading.Timer):
  def __init__(self, delay, fn, origin, silent = False, *args):
    self.delay = delay
    self.origin = origin
    self.silent = silent
    threading.Timer.__init__(self, self.assign_interval(), fn, args=(self, args))
    self.name = None

  def run(self):
    while not self.finished.wait(self.interval):
      if self.origin.enabled:
        if not self.silent:
          print(f" >> {self.name} {self.interval_str}")
        self.function(self.origin, *self.args, **self.kwargs)
        self.assign_interval()

  def calculate_delay(self):
    if isinstance(self.delay, list):
      return random.uniform(self.delay[0], self.delay[1])

    return self.delay

  def assign_interval(self):
    self.interval = self.calculate_delay()
    self.interval_str = float_format.format(self.interval)
    return self.interval

def task_listener(delay, silent=False):
  def wrapper(fn):
    @wraps(fn)
    def wrapped(self, *f_args, **f_kwargs):
      timer = timers.get(fn.__name__)
      if not timer:
        timer = task_timer(delay, fn, self, silent, *f_args, **f_kwargs)
        timers[fn.__name__] = timer
      timer.start()
      return timer
    return wrapped
  return wrapper

class torambot:
  def __init__(self):
    self.enabled = True
    self.settings = settings
    self.name = "ToramOnline"
    self.app = Application(backend="win32").connect(title=self.name, timeout=10)
    self.window = self.app.window(title=self.name)
    #print(self.window.write_to_xml("test.xml"))

  def is_active(self):
    return self.name in window_current()

  def print(self, msg, *args, clearLine=False):
    end = clearLine and '\r' or '\n'
    print(msg, *args, end=end, flush=True)
    if clearLine:
      sys.stdout.write("\033[K")

  def toggle_handler(self, call):
    self.enabled = not self.enabled
    if self.enabled:
      print(" Enabled"+string_repeat(' ', 30))
    else:
      print(" Disabled"+string_repeat(' ', 30))

  def quit_handler(self, call):
    print("\n quitting"+string_repeat(' ', 30))
    # a normal exit won't work if the program hangs, need to do this
    os.kill(os.getpid(), signal.SIGTERM)

  @task_listener(delay=[1, 4])
  def auto_attack_task(self, *args):
    self.window.send_keystrokes("f")
    time.sleep(random.uniform(0.15, 0.22))
    self.window.send_keystrokes("f")

  @task_listener(delay=[10, 18])
  def attack_1_task(self, *args):
    config = args[0].config
    press_count = config.get("press_count") or [2,4]
    for x in range(random.randrange(press_count[0],press_count[1])):
      print("  --> send_keystrokes('1')")
      self.window.send_keystrokes("1")
      time.sleep(random.uniform(0.21, 0.32))
      self.window.send_keystrokes("1")
      time.sleep(random.uniform(1.5, 3))
    else:
      follow_up = config.get("follow_up")
      if not follow_up or not follow_up.get("enabled"):
        return
      chance = follow_up.get("chance") or 0.35
      if random.uniform(0, 1) <= chance:
        if follow_up.get("type") or "keystroke" == "keystroke":
          key = follow_up.get("key") or "e"
          fdelay = follow_up.get("delay") or [0,0]
          time.sleep(random.uniform(fdelay[0], fdelay[1]))
          print(f"  --> send_keystrokes('{key}')")
          self.window.send_keystrokes(key)

  @task_listener(delay=[30, 60])
  def rotate_camera(self, *args):
    direction = random.choice(["VK_LEFT", "VK_RIGHT"])
    self.window.send_keystrokes("{" + direction + " down}")
    time.sleep(random.uniform(0.8, 1))
    self.window.send_keystrokes("{" + direction + "}")

  @task_listener(delay=0.8, silent=True)
  def info_gathering(self, *args):
    self.window.set_focus()
    img = self.window.capture_as_image()
    img.save("test.png")
    coord = x, y = 954, 944
    pixel = img.getpixel(coord)
    print(pixel)
    #R:104,G:234,B:212

    if (is_within(pixel[0], 23, 15) and is_within(pixel[1], 31, 15) and is_within(pixel[2], 26, 15)):
      self.window.send_keystrokes("e")


#a is with b +- range
def is_within(a, b, rng):
  return a >= (b - rng) and a <= (b + rng)

def process_tasks(tasks, parent=None):
  if not tasks:
    return False

  for name in tasks:
    task_config = tasks.get(name)
    enabled = task_config.get("enabled")
    if not enabled:
      continue
    # run the task
    fqn = (parent and type(parent).__name__ + "." or "") + name
    if parent:
      func = getattr(parent, name)
    else:
      func = globals()[name]
    if not func:
      continue
    timer = parent and func() or func(main)
    if timer:
      timer.name = fqn
      timer.config = task_config
      delay = task_config.get("delay")
      if delay:
        timer.delay = delay
        timer.interval = delay
      print(f" Starting {fqn}")
      print(f"   delay: {timer.delay}")

  print()
  return True

def load_main():
  global main
  main = task_classes.get("torambot")
  if not main:
    print("torambot not found, creating")
    main = torambot()
    task_classes["torambot"] = main

  main.info_gathering()
  return main


if __name__ == "__main__":
  print("")
  print(" Welcome to")
  print(" _____                   _____     _   \n|_   _|___ ___ ___ _____| __  |___| |_ \n  | | | . |  _| .\'|     | __ -| . |  _|\n  |_| |___|_| |__,|_|_|_|_____|___|_|  \n                                       ")
  
  keybinds = settings["keybinds"]

  # enable listening to keyboard and mouse events
  for action in keybinds:
    key = keybinds[action]
    print(f" press {key} to {action}")
  print()

  # register tasks
  tasks = []
  for name in settings:
    parent = settings.get(name)
    if name != "tasks":
      if not parent.get("enabled"):
        continue
      # create task class
      klass = globals()[name]
      if klass:
        task_classes[name] = klass()
      process_tasks(parent.get("tasks"), task_classes[name])
    else:
      tasks.append(parent)

  load_main()
    
  for task in tasks:
    process_tasks(task)

  keyboard.on_release_key(keybinds["pause"], main.toggle_handler)
  keyboard.on_release_key(keybinds["quit"],  main.quit_handler)
