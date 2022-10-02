# system
import random
import time

# core
from pybot.core.component import TaskComponent

class BreakTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.chance = config.get("chance") or 0.25
    self.delay = config.get("delay") or [20, 200]

  def update(self, task):
    super().update(task)
    
    if random.uniform(0, 1.0) <= self.chance:
      time.sleep(random.uniform(self.delay[0], self.delay[1]))

  def post_update(self, task):
    super().post_update(task)
