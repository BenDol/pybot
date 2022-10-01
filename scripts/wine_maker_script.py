# system
import random
import time

# core
from script import Script
from tasks import task
from tasks import TaskHandler

#util
import util.color as color

class WineMakerScript(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)
    self.bag_open = False

  def load(self, conf):
    super().load(conf)

  def unload(self):
    super().unload()

  @task(delay=[1,3], silent=True)
  def test(self, *args):
    print("force")
    self.run_task("open_bag")

  @task(delay=[1,3], silent=True)
  def open_bag(self, *args):
    def can_start():
      print("can_start")
      bag_icon = self.game.screen_capture.getpixel((2324, 904))
      return not color.is_match(bag_icon, [111, 37, 28], 10)
    def started():
      print("started")
    def completed():
      print("completed")
      bag_icon = self.game.screen_capture.getpixel((2324, 904))
      self.bag_open = color.is_match(bag_icon, [111, 37, 28], 10)
    def failed(err):
        print("failed " + err)
    return TaskHandler(can_start=can_start, started=started, completed=completed, failed=failed)
