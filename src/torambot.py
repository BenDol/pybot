import os
import signal
import threading
import time
import datetime
import random
import sys

import keyboard
import mouse as m
from util.mouse import *
from pynput import mouse
from pywinauto.application import Application
from pywinauto import win32defines
from functools import wraps

from util.win32 import window_current
from util.string import string_repeat

from settings import settings as settings

os.system('mode con: cols=100 lines=41')

timers = {}

float_format = "{0:.2f}"

class task_timer(threading.Timer):
  def __init__(self, delay, fn, origin, *args):
    self.delay = delay
    self.origin = origin;
    threading.Timer.__init__(self, self.assign_interval(), fn, args=(self, args))

  def run(self):
    while not self.finished.wait(self.interval):
      if self.origin.enabled:
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

def task_listener(delay):
  def wrapper(fn):
    @wraps(fn)
    def wrapped(self, *f_args, **f_kwargs):
      timer = timers.get(fn.__name__)
      if not timer:
        timer = task_timer(delay, fn, self, *f_args, **f_kwargs)
        timers[fn.__name__] = timer
      timer.start()
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
    mouse_track_end()
    # a normal exit won't work if the program hangs, need to do this
    os.kill(os.getpid(), signal.SIGTERM)

  @task_listener(delay=[1, 4])
  def auto_attack_task(self, *args):
    self.print(f"attack_task {args[0].interval_str}s")
    self.window.send_keystrokes("f")
    time.sleep(random.uniform(0.15, 0.22))
    self.window.send_keystrokes("f")

  @task_listener(delay=[10, 18])
  def attack_1_task(self, *args):
    self.print(f"attack_1_task {args[0].interval_str}s")
    for x in range(random.randrange(2,4)):
      self.print("send_keystrokes('1')")
      self.window.send_keystrokes("1")
      time.sleep(random.uniform(0.15, 0.22))
      self.window.send_keystrokes("1")
      time.sleep(random.uniform(1.5, 3))
    else:
      if (random.randrange(0, 100) <= 35):
        self.window.send_keystrokes("e")

  @task_listener(delay=[30, 60])
  def rotate_camera(self, *args):
    direction = random.choice(["VK_LEFT", "VK_RIGHT"])
    self.print(f"rotate_camera {direction} {args[0].interval_str}s")
    self.window.send_keystrokes("{" + direction + " down}")
    time.sleep(random.uniform(0.8, 1))
    self.window.send_keystrokes("{" + direction + "}")


if __name__ == "__main__":
  print("")
  print(" Welcome to")
  print("                                       \n _____                   _____     _   \n|_   _|___ ___ ___ _____| __  |___| |_ \n  | | | . |  _| .\'|     | __ -| . |  _|\n  |_| |___|_| |__,|_|_|_|_____|___|_|  \n                                       ")
  main = torambot()
  print(" press F12 to quit")
  print(" press F10 to pause\n")
  
  # enable listening to keyboard and mouse events
  keyboard.on_release_key('F10', main.toggle_handler)
  keyboard.on_release_key('F12', main.quit_handler)

  # register tasks
  main.auto_attack_task()
  #main.attack_1_task()
  main.rotate_camera()