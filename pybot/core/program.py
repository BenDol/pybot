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

# extern
import pywinauto
from pywinauto.application import Application

# core
import pybot.core.tasks as tasks
from pybot.core.tasks import task
from pybot.core.tasks import TaskHandler
from pybot.core.mouse import PyWinMouse

# util
import pybot.util.win32 as win32
import pybot.util.color as color

class Program(object):
  def __init__(self, config):
    self.enabled = True
    self.config = config
    self.name = config.get("title")
    self.data = {}
    self.tasks = []
    self.app = None
    self.window = None
    self.mouse = None
    self.screen_capture = None
    # print(self.window.write_to_xml("test.xml"))

  def load(self):
    self.attach()

    if not self.mouse:
      self.mouse = PyWinMouse(pywinauto.mouse)

    if self.window:
      print(f" Successfully attached!")
    print()

    # Load tasks
    t = self.config.get("tasks")
    if t:
      self.tasks = tasks.process(t, self)

  def start(self):
    print(f" Starting Program")
    for task in self.tasks:
      task.start()
      print(f"  -> Task '{task.name}'")
      print(f"     Delay: {task.delay}")

  def attach(self):
    print(f" Attaching to '{self.name}' ...")
    # Attach to application
    self.app = Application(backend="win32").connect(title=self.name, timeout=10)
    self.window = self.app.window(title=self.name)

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

class NoProgram(Program):
  def __init__(self, config):
    super().__init__(config)

  def load(self):
    super().load()

  def attach(self):
    pass # dont attach