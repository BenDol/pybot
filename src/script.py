# system
import time
import random
import json

# core
import tasks
import components

class Script(object):
  def __init__(self, parent, config, namespace=None):
    self.name = type(self).__name__
    self.namespace = namespace
    self.parent = parent
    self.game = parent.game
    self.config = config
    self.enabled = False
    self.tasks = {}
    self.verbose = False
    self.components = []

  def load(self):
    print(f" Loading {self.name}")
    self.enabled = self.config.get("enabled")
    self.verbose = self.config.get("verbose")
    
    # load components
    comp_list = self.config.get("components")
    if (comp_list):
      for c in comp_list:
        components.add(self, c["name"], c["config"] or {})

    # load tasks
    t = self.config.get("tasks")
    if self.verbose:
      print(f" {json.dumps(t, indent=2, sort_keys=False)}")
    if t:
      self.tasks = tasks.process(t, self)

  def unload(self):
    self.print(f"Unloading {self.name}", False)

  def start(self):
    self.print(f"Starting {self.name}", False)
    for task in self.tasks:
      task.start()
      print(f"  -> Task '{task.name}'")
      print(f"     Delay: {task.delay}")

  def stop(self):
    self.print(f"Stopping {self.name}", False)

  def print(self, msg, namespace=True):
    if namespace:
      print(f" [{self.namespace}.py] {msg}")
    else:
      print(f" {msg}")

  def config_value(self, key, or_default=None, config=None):
    if not config:
      config = self.config
    value = config.get(key)
    return value and value or or_default

  def send_keystrokes(self, key, delay=None):
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))
    self.game.window.send_keystrokes(key)
