# system
import os
import sys
import inspect
import importlib

# util
import util.string as string

loaded = False
modules = []
classes = {}
components = []

sys.path.append("scripts/components")

class Component(object):
  def __init__(self, config):
    self.config = config
    self.enabled = config["enabled"]

  def load(self):
    pass

  def unload(self):
    pass

  def update(self):
    pass

  def post_update(self):
    pass

class TaskComponent(Component):
  def __init__(self, config):
    super().__init__(config)

  def load(self):
    super().load()

  def unload(self):
    super().unload()

  def update(self, task):
    super().update()

  def post_update(self, task):
    super().post_update()

def load(path="scripts/components"):
  for file_name in os.listdir(path):
    module_name = file_name.replace(".py", "")
    module = importlib.import_module(module_name)
    if module:
      modules.append(module)

    # load script classes
    for name, obj in inspect.getmembers(module):
      if not inspect.isclass(obj):
        continue
      if obj is Component or not issubclass(obj, Component):
        continue
      if obj is TaskComponent or not issubclass(obj, TaskComponent):
        continue
      classes[name] = obj
  else:
    loaded = True

def add(owner, component_name, indent=1, *args):
  indent_str = string.repeat(' ', indent)
  clazz = classes[component_name]
  if not clazz:
    print(f"{indent_str}Component '{component_name}' not found")
    return None

  comp = clazz(*args)
  comp.load()
  components.append(comp)

  if owner.components is None:
    throw_no_components()

  owner.components.append(comp)
  print(f"{indent_str}Added component '{component_name}' to {owner}")
  return comp

def get(owner, component_name):
  if owner.components is None:
    throw_no_components()

  for comp in owner.components:
    if type(comp).__name__ is component_name:
      return comp
  return None

def throw_no_components(owner):
  raise RuntimeError(f" Owner '{owner}' does not have a 'components' list member")