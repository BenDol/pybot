# system
import random
import time

# core
from script import Script
from tasks import task

class Attack1(Script):
  def __init__(self, parent, config):
    Script.__init__(self, parent, config, __name__)

  def load(self):
    Script.load(self)

  def unload(self):
    Script.load(self)

  @task(delay=[10,18])
  def attack(self, *args):
    task = args[0]
    key = self.config_value("key", "f", task.config)
    press_count = task.config.get("press_count") or [2,4]
    for x in range(random.randrange(press_count[0],press_count[1])):
      print("  --> send_keystrokes('1')")
      self.send_keystrokes("1")
      time.sleep(random.uniform(0.21, 0.32))
      self.send_keystrokes("1")
      time.sleep(random.uniform(1.5, 3))
    else:
      follow_up = task.config.get("follow_up")
      if not follow_up or not follow_up.get("enabled"):
        return
      chance = follow_up.get("chance") or 0.35
      if random.uniform(0, 1) <= chance:
        if follow_up.get("type") or "keystroke" == "keystroke":
          key = follow_up.get("key") or "e"
          fdelay = follow_up.get("delay") or [0,0]
          time.sleep(random.uniform(fdelay[0], fdelay[1]))
          print(f"  --> send_keystrokes('{key}')")
          self.send_keystrokes(key)
