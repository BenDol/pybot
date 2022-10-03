# Copyright (c) 2021-2022 PyBot <https://github.com/BenDol/pybot>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# system
import os
import signal
import sys
import inspect
import importlib

# core
import pybot.core.tasks as tasks
import pybot.core.config as config
from pybot.core.program import Program
from pybot.core.program import NoProgram
from pybot.core.component import Component
from pybot.core.component import TaskComponent
from pybot.core.settings import settings as settings
from pybot.core.script import Script

# extern
import keyboard

# utils
import pybot.util.string as string

#os.system('mode con: cols=100 lines=41')

sys.path.append("scripts")
sys.path.append("scripts/components")
sys.path.append("scripts/programs")

app = None

class App:
  def __init__(self):
    self.enabled = True
    self.settings = settings
    self.program = None
    self.scripts = []
    self.components = []
    self.component_classes = {}
    self.component_modules = []
    self.program_modules = []
    self.program_classes = {}
    self.keybinds = {}
    tasks.app = self

  def is_active(self):
    return self.program.is_active()

  def enable(self, enabled):
    if enabled:
      print(" Enabled" + string.repeat(' ', 20))
    else:
      print(" Disabled" + string.repeat(' ', 20))

    self.enabled = enabled
    self.program.enabled = enabled

    for script in self.scripts:
      script.enabled = enabled

  def toggle(self, *args):
    self.enable(not self.enabled)

  def quit(self, *args):
    print(" >> Quitting" + string.repeat(' ', 20))
    print()
    # a normal exit won't work if the program hangs, need to do this
    os.kill(os.getpid(), signal.SIGTERM)

  def load(self):
    self.keybinds = settings["keybinds"]
    keyboard.on_release_key(self.keybinds["pause"], app.toggle)
    keyboard.on_release_key(self.keybinds["quit"],  app.quit)

    # enable listening to keyboard and mouse events
    for action in self.keybinds:
      key = self.keybinds[action]
      print(f" press {key} to {action}")
    print()

    self.load_programs()

    # Load program
    self.program = self.create_program()
    self.program.load()

    # load components
    self.load_components()

    # Load scripts
    self.load_scripts()

  def start(self):
    # Start program
    self.program.start()

    # Start scripts
    self.start_scripts()

  def load_programs(self, path="scripts/programs"):
    for file_name in os.listdir(path):
      name = file_name.replace(".py", "")
      module = importlib.import_module(name)
      if module:
        self.program_modules.append(module)

      # load script classes
      for n, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
          continue
        if obj is Program or not issubclass(obj, Program):
          continue
        self.program_classes[n] = obj

  def create_program(self):
    prog_conf = settings.get('program')
    if not prog_conf:
      return NoProgram({})
    class_name = prog_conf.get('class')
    if not class_name:
      return NoProgram(prog_conf)
    program = self.program_classes[class_name]
    return program(prog_conf)

  def load_scripts(self):
    configs = self.settings.get("scripts")
    if not configs:
      return

    for name in configs:
      conf = configs[name]
      module = importlib.import_module(name)
      # load script classes
      for n, obj in inspect.getmembers(module):
        if obj is Script or not inspect.isclass(obj) or not issubclass(obj, Script):
          continue

        script = obj(self, config.load("scripts/" + name))
        script.load(conf)
        self.scripts.append(script)
    count = len(self.scripts)
    print(f" Loaded {count} script class{'es'[:count^1]}")
    print()

  def start_scripts(self):
    count = 0
    for script in self.scripts:
      if script.enabled:
        script.start()
        count += 1
    print()
    print(f" Started {count} script{'s'[:count^1]}")
    print()

  def load_components(self, path="scripts/components"):
    for file_name in os.listdir(path):
      name = file_name.replace(".py", "")
      module = importlib.import_module(name)
      if module:
        self.component_modules.append(module)

      # load script classes
      for n, obj in inspect.getmembers(module):
        if not inspect.isclass(obj):
          continue
        if obj is Component or not issubclass(obj, Component):
          continue
        if obj is TaskComponent or not issubclass(obj, TaskComponent):
          continue
        self.component_classes[n] = obj

  def add_component(self, owner, component_name, indent=1, *args):
    clazz = self.component_classes[component_name]
    if not clazz:
      print(f"{string.indent(indent)}Component '{component_name}' not found")
      return None

    comp = clazz(*args)
    comp.load(owner)
    self.components.append(comp)

    if owner.components is None:
      throw_no_components(owner)

    owner.components.append(comp)
    print(f"{string.indent(indent)}Added component '{component_name}'")
    return comp

  def get_component(self, owner, component_name):
    if owner.components is None:
      throw_no_components(owner)

    for comp in owner.components:
      if type(comp).__name__ is component_name:
        return comp
    return None

def throw_no_components(owner):
  raise RuntimeError(f" Owner '{owner}' does not have a 'components' list member")

def main():
  print("")
  print(" Welcome to")
  print("  _______  __   __  _______  _______  _______ \n |       ||  | |  ||  _    ||       ||       |\n |    _  ||  |_|  || |_|   ||   _   ||_     _|\n |   |_| ||       ||       ||  | |  |  |   |  \n |    ___||_     _||  _   | |  |_|  |  |   |  \n |   |      |   |  | |_|   ||       |  |   |  \n |___|      |___|  |_______||_______|  |___|  \n  \n                                       ")

  global app
  app = App()
  app.load()
  app.start()

if __name__ == "__main__":
  main()