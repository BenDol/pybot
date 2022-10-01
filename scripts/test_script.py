# system
import random
import time

# core
from script import Script
from tasks import task

class Test(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)

  def load(self):
    super().load()

  def unload(self):
    super().unload()

  @task(delay=[1,3])
  def move(self, *args):
    return False
