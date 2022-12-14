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
import threading
import random

# extern
from functools import wraps

# core
from pybot.core.settings import settings as settings

float_format = "{0:.2f}"

configs = {}
tasks = {}
globes = globals()
app = None

class Task(threading.Timer):
  def __init__(self, delay, fn, origin, name, silent=False, *args):
    self.interval_str = None
    self.finished = None
    self.delay = delay
    self.origin = origin
    self.silent = silent
    self.running = False
    if hasattr(origin, 'program'):
      self.program = origin.program
    else:
      self.program = origin
    super().__init__(self.assign_interval(), fn, args=(self, args))
    self.name = name
    self.components = []

  def run(self):
    while not self.finished.wait(self.interval):
      self.running = self.origin.enabled
      if self.origin.enabled:
        if not self.silent:
          print(f" >> {self.name} {self.interval_str}s")

        handler = self.function(self.origin, *self.args, **self.kwargs)
        try:
          if handler and handler.can_start(self):
            handler.on_started(self)
            self.components_update()
            self.components_post_update()
            handler.on_completed(self)
        except Exception as e:
          print(f" ERROR: task '{self.name}' failed => {str(e)}")
          handler.on_failed(self, e)

        self.assign_interval()
    else:
      self.running = False

  def cancel(self):
    super().cancel()
    self.running = False

  def calculate_delay(self):
    if isinstance(self.delay, list):
      return random.uniform(self.delay[0], self.delay[1])

    return self.delay

  def assign_interval(self):
    self.interval = self.calculate_delay()
    self.interval_str = float_format.format(self.interval)
    return self.interval

  def components_update(self):
    for c in self.components:
      if not c.enabled:
        continue
      if c.parallel:
        thread = threading.Thread(target=lambda: c.update(self))
        thread.start()
      else:
        c.update(self)

  def components_post_update(self):
    for c in self.components:
      if not c.enabled:
        continue
      if c.parallel:
        thread = threading.Thread(target=lambda: c.post_update(self))
        thread.start()
      else:
        c.post_update(self)


class TaskHandler(object):
  def __init__(self, can_start=lambda t: True, started=None, completed=None, failed=None):
    self.can_start = can_start
    self.started = started
    self.completed = completed
    self.failed = failed

  def on_started(self, task):
    if self.started:
      self.started(task)

  def on_completed(self, task):
    if self.completed:
      self.completed(task)

  def on_failed(self, task, e):
    if self.failed:
      self.failed(task, e)

def task(delay, silent=False):
  def wrapper(fn):
    @wraps(fn)
    def wrapped(self, *f_args, **f_kwargs):
      fqn = type(self).__name__ + "." + fn.__name__
      task = tasks.get(fqn)
      if not task:
        task = Task(delay, fn, self, fqn, silent, *f_args, **f_kwargs)
        tasks[fn.__name__] = task
      return task
    return wrapped
  return wrapper


def add_globals(globs):
  globes.update(globs)


def process(tasks, parent=None):
  if not tasks:
    return None

  instances = []
  for name in tasks:
    task_config = tasks.get(name)
    enabled = task_config.get("enabled")
    if not enabled:
      continue
    # run the task
    fqn = (parent and type(parent).__name__ + "." or "") + name
    if parent:
      func = getattr(parent, name)
    else:
      func = globes[name]
    if not func:
      continue

    if parent:
      task = func()
    else:
      task = func(app)

    if not task:
      continue
    task.config = task_config
    delay = task_config.get("delay")
    if delay:
      task.delay = delay
      task.assign_interval()

    # load components
    comp_list = task_config.get("components")
    if (comp_list):
      for c in comp_list:
        app.add_component(task, c["name"], 3, c["config"] or {})

    instances.append(task)
  return instances

def task_running(name):
  task = get_task(name)
  return task and task.running

def task_exists(name):
  return get_task(name) is not None

def task_enabled(name):
  task = get_task(name)
  return task and task.enabled

def get_task(name):
  return tasks.get(name)
