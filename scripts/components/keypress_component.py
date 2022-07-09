# system
import random
import time

# core
from components import TaskComponent

class KeyPressTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.key = self.config["key"]
    self.presses = self.config.get("presses") or 1
    self.delay = self.config.get("delay") or [0.21, 0.32]
    self.post_delay = self.config.get("post_delay") or [2, 4]

  def update(self, task):
    for x in range(self.presses):
      task.origin.send_keystrokes(self.key)
      if x != self.presses:
        time.sleep(random.uniform(self.delay[0], self.delay[1]))
    else:
      time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    pass
