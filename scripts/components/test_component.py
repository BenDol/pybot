# system
import random
import time

# core
from components import TaskComponent

class TestTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)

  def update(self, task):
    super().update(task)
    print("test update")
    time.sleep(30)
    print("test update ended")

  def post_update(self, task):
    super().post_update(task)
    print("test post_update")
