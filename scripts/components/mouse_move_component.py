# system
import random
import time

# core
from pybot.core.component import TaskComponent

#util
import pybot.util.vector as vector

class MouseMoveTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.position   = self.config.get("position")   or None
    self.speed      = self.config.get("speed")      or [25, 55]
    self.delay      = self.config.get("delay")      or None
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    if self.position:
      if len(self.position) == 2:
        self.game.mouse.navigate(xy=(self.position[0], self.position[1]), speed=self.speed, delay=self.delay)
      else:
        self.last_pos = vector.random_point((self.position[0], self.position[1]), (self.position[2], self.position[3]))
        self.game.mouse.navigate(xy=(self.last_pos[0], self.last_pos[1]), speed=self.speed, delay=self.delay)

    time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
