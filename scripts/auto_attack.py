# system
import random
import time

# core
from script import Script
from tasks import task

class AutoAttack(Script):
  def __init__(self, parent, config):
    Script.__init__(self, parent, config, __name__)

  def load(self):
    Script.load(self)

  def unload(self):
    Script.load(self)

  @task(delay=[1,3])
  def attack(self, *args):
    task = args[0]
    key = self.config_value("key", "f", task.config)
    self.send_keystrokes(key)
    self.send_keystrokes(key, [0.15, 0.22])
