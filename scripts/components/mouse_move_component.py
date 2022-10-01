# system
import random
import time

# core
from components import TaskComponent

class MouseMoveTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.pos = self.config.get("pos") or None
    self.delay = self.config.get("delay") or None
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    print("update")

    self.game.mouse.navigate(xy=(self.pos[0], self.pos[1]), delay=self.delay)

    time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
