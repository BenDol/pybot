# system
import random
import time

# core
from pybot.core.component import TaskComponent

class KeyPressTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.key = self.config["key"]
    self.presses = self.config.get("presses") or 1
    self.hold = self.config.get("hold") or False
    self.delay = self.config.get("delay") or [0.21, 0.32]
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    for x in range(self.presses):
      raw_key = self.get_key()
      key = "{" + raw_key + (self.hold and " down" or "") + "}"
      self.program.send_keystrokes(key)
      if x != self.presses:
        time.sleep(random.uniform(self.delay[0], self.delay[1]))
      if self.hold:
        self.program.send_keystrokes("{"+raw_key+"}")
    else:
      time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)

  def get_key(self):
    return isinstance(self.key, list) and random.choice(self.key) or self.key
