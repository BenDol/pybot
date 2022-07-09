# system
import random
import time

# core
from script import Script
from tasks import task

class Unstuck(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)

  def load(self):
    Script.load(self)

  def unload(self):
    Script.load(self)

  @task(delay=[30, 60])
  def rotate_camera(self, *args):
    pass