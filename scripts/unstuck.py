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

  @task(delay=[30,60])
  def rotate_camera(self, *args):
    task = args[0]
    direction = random.choice(["VK_LEFT", "VK_RIGHT"])
    self.send_keystrokes("{" + direction + " down}")
    time.sleep(random.uniform(0.8, 1))
    self.send_keystrokes("{" + direction + "}")
