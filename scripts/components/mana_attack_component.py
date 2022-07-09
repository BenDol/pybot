# system
import random
import time

# core
from components import TaskComponent

class ManaAttackTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)

  def update(self, task):
    game = task.origin.game
    while game.data.get("mana") and game.data.get("mana") < 42:
      #print(game.data["mana"])
      task.origin.send_keystrokes("e")
      time.sleep(random.uniform(8, 9))
    
    task.origin.send_keystrokes("1")
    time.sleep(random.uniform(0.21, 0.32))
    task.origin.send_keystrokes("1")
    time.sleep(random.uniform(2, 4))

  def post_update(self, task):
    print("post_update")
