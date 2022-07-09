# system
import random
import time

# core
from components import TaskComponent

class ManaChargeTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.key = self.config.get("key") or "e"
    self.mana = self.config.get("mana") or 42
    self.post_delay = self.config.get("post_delay") or [8, 9]

  def update(self, task):
    super().update(task)

    game = task.origin.game
    while game.data.get("mana") and game.data.get("mana") < self.mana:
      #print(game.data["mana"])
      task.origin.send_keystrokes(self.key)
      time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
