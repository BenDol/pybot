# core
from pybot.core.program import Program
from pybot.core.tasks import task
from pybot.core.tasks import TaskHandler

class Runescape(Program):
  def __init__(self, config):
    super().__init__(config)

  @task(delay=0.5, silent=True)
  def scan(self, *args):
    super().scan(*args)
    return TaskHandler()
