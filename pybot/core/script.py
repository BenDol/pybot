# system
import time
import random
import json

# core
import pybot.core.tasks as tasks

class Script(object):
  def __init__(self, parent, config, namespace=None):
    self.name = type(self).__name__
    self.namespace = namespace
    self.parent = parent
    self.program = parent.program
    self.config = config
    self.enabled = False
    self.tasks = {}
    self.verbose = False
    self.components = []

  def load(self, config):
    print(f" Loading {self.name}")
    self.config = self.config | config
    self.enabled = self.config.get("enabled")
    self.verbose = self.config.get("verbose")

    # load components
    comp_list = self.config.get("components")
    if (comp_list):
      for c in comp_list:
        parent.add_component(self, c["name"], 3, c["config"] or {})

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

  def run_task(self, name):
    if callable(name):
      name = name.__name__
    for task in self.tasks:
      if task.name.endswith(name):
        print("found")
        task.run()

  def send_keystrokes(self, key, delay=None):
    self.program.send_keystrokes(key, delay)
