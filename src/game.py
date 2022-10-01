# extern
import pywinauto
from pywinauto.application import Application

# core
import tasks
from tasks import task
from tasks import TaskHandler
from mouse import PyWinMouse

# util
import util.win32 as win32
import util.color as color

class Game(object):
  def __init__(self, config):
    self.enabled = True
    self.config = config
    self.name = config["title"]
    self.data = {}
    self.tasks = None
    self.app = None
    self.window = None
    self.mouse = None
    self.screen_capture = None
    # print(self.window.write_to_xml("test.xml"))

  def load(self):
    print(f" Attaching to '{self.name}' ...")
    # Attach to application
    self.app = Application(backend="win32").connect(title=self.name, timeout=10)
    self.window = self.app.window(title=self.name)
    if not self.mouse:
      self.mouse = PyWinMouse(pywinauto.mouse)

    if self.window:
      print(f" Successfully attached!")
    print()

    # Load tasks
    t = self.config.get("tasks")
    self.tasks = tasks.process(t, self)

  def start(self):
    print(f"Starting Game")
    for task in self.tasks:
      task.start()
      print(f"  -> Task '{task.name}'")
      print(f"     Delay: {task.delay}")

  def is_active(self):
    return self.name in win32.window_current()

  def scan(self, *args):
    self.screen_capture, result = win32.capture_screen(self.name)
    # if result:
    #  self.screen_capture.save("testing.png")

  def send_keystrokes(self, key, delay=None):
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))
    self.window.send_keystrokes(key)

  def mouse_move(self, xy, delay=None):
    self.mouse.move(coords=xy)

  def mouse_click(self, button='left', delay=None):
    self.mouse.click(button, delay)


class RunescapeGame(Game):
  def __init__(self, config):
    super().__init__(config)

  @task(delay=0.5, silent=True)
  def scan(self, *args):
    Game.scan(self, *args)
    return TaskHandler()

class ToramGame(Game):
  def __init__(self, config):
    super().__init__(config)
    self.health_chunks = [
      [686, 731],
      [742, 787],
      [797, 841],
      [853, 897],
      [909, 953],
      [964, 1008],
      [1020, 1064],
      [1075, 1120],
      [1131, 1175],
      [1186, 1231]
    ]

  @task(delay=0.5, silent=True)
  def scan(self, *args):
    Game.scan(self, *args)
    self.data["mana"] = self.read_mana()
    return TaskHandler()

  def read_mana(self):
    if not self.is_health_showing():
      return

    total = 0
    amount = 0

    for chunk in self.health_chunks:
      start = chunk[0]
      end = chunk[1]

      for x in range(start, end):
        total += 1
        for rgb in [[105, 237, 213], [108, 246, 95]]:
          pixel = self.screen_capture.getpixel((x, 913))
          if color.is_match(pixel, rgb, 20):
            amount += 1
            break

    percent = (amount / total) * 100
    # print("amount: " + str(amount))
    # print("total: " + str(total))
    # print("percent: " + str(percent))
    return percent

  def is_health_showing(self):
    rgb = [58, 152, 65]
    pixel = self.screen_capture.getpixel((685, 875))
    return color.is_match(pixel, rgb, 0)
