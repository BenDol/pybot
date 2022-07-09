# system
import random
import time

# core
from script import Script
from tasks import task

class Attack1(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)

  def load(self):
    Script.load(self)

  def unload(self):
    Script.load(self)

  @task(delay=[10,18])
  def attack(self, *args):
    pass
  