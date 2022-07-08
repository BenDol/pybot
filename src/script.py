# system
import time
import random
import json

# core
import tasks

class Script(object):
  def __init__(self, parent, config, namespace):
    self.name = type(self).__name__
    self.namespace = namespace
    self.parent = parent
    self.config = config
    self.enabled = False
    self.tasks = {}
    self.verbose = False

  def load(self):
    print(f" Loading {self.name}")
    self.enabled = self.config.get("enabled")
    self.verbose = self.config.get("verbose")
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
      print(f"  -> Task {task.name}")
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

  def send_keystrokes(self, key, delay=[]):
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))
    self.parent.window.send_keystrokes(key)