# system
import random
import time

# core
from components import TaskComponent

# components
from mouse_move_component import MouseMoveTaskComponent

class MouseClickTaskComponent(MouseMoveTaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.button = self.config.get("button") or 'left'

  def update(self, task):
    super().update(task)

    self.game.mouse.click(button=self.button, delay=self.delay)

    time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
