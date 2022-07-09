# system
import threading
import random

# extern
from functools import wraps

# core
import components
from settings import settings as settings

float_format = "{0:.2f}"

configs = {}
tasks = {}
globes = globals()
main = None

class Task(threading.Timer):
  def __init__(self, delay, fn, origin, name, silent=False, *args):
    self.interval_str = None
    self.finished = None
    self.delay = delay
    self.origin = origin
    self.silent = silent
    self.running = False
    super().__init__(self.assign_interval(), fn, args=(self, args))
    self.name = name
    self.components = []

  def run(self):
    while not self.finished.wait(self.interval):
      self.running = self.origin.enabled
      if self.origin.enabled:
        if not self.silent:
          print(f" >> {self.name} {self.interval_str}s")

        for c in self.components:
          if c.enabled:
            c.update(self)

        self.function(self.origin, *self.args, **self.kwargs)

        for c in self.components:
          if c.enabled:
            c.post_update(self)

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
      task = func(main)

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
        components.add(task, c["name"], c["config"] or {})

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
