# system
import threading
import random

# extern
from functools import wraps

# core
from settings import settings as settings

float_format = "{0:.2f}"

configs = {}
timers = {}
all_globals = globals()

class task_timer(threading.Timer):
  def __init__(self, delay, fn, origin, silent = False, *args):
    self.delay = delay
    self.origin = origin
    self.silent = silent
    threading.Timer.__init__(self, self.assign_interval(), fn, args=(self, args))
    self.name = None

  def run(self):
    while not self.finished.wait(self.interval):
      if self.origin.enabled:
        if not self.silent:
          print(f" >> {self.name} {self.interval_str}")
        self.function(self.origin, *self.args, **self.kwargs)
        self.assign_interval()

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
      timer = timers.get(fqn)
      if not timer:
        timer = task_timer(delay, fn, self, silent, *f_args, **f_kwargs)
        timers[fn.__name__] = timer
      return timer
    return wrapped
  return wrapper

def add_globals(globs):
  all_globals.update(globs)

# load tasks and return late load tasks for loading after main
def load():
  tasks = []
  for name in settings:
    parent = settings.get(name)
    if name != "tasks":
      if not parent.get("enabled"):
        continue
      # create task class
      klass = all_globals[name]
      if klass:
        configs[name] = klass()
      process(parent.get("tasks"), configs[name])
    else:
      tasks.append(parent)

  return tasks

def process(tasks, parent=None):
  if not tasks:
    return None

  timers = []

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
      func = all_globals[name]
    if not func:
      continue
    timer = parent and func() or func(main)
    if timer:
      timer.name = fqn
      timer.config = task_config
      delay = task_config.get("delay")
      if delay:
        timer.delay = delay
        timer.assign_interval()
      timers.append(timer)
  return timers