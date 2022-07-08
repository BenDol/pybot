# system
import random
import time

# core
from script import Script
from tasks import task

class Attack1(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)

  def load(self):
    Script.load(self)

  def unload(self):
    Script.load(self)

  @task(delay=[10,18])
  def attack(self, *args):
    while self.game.data.get("mana") and self.game.data.get("mana") < 42:
      #print(self.game.data["mana"])
      self.send_keystrokes("e")
      time.sleep(random.uniform(8, 9))
    
    self.send_keystrokes("1")
    time.sleep(random.uniform(0.21, 0.32))
    self.send_keystrokes("1")
    time.sleep(random.uniform(2, 4))
  