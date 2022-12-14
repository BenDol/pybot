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
import random
import time

# core
from pybot.core.component import TaskComponent

class KeyPressTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.key = self.config["key"]
    self.presses = self.config.get("presses") or 1
    self.hold = self.config.get("hold") or False
    self.delay = self.config.get("delay") or [0.21, 0.32]
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    for x in range(self.presses):
      raw_key = self.get_key()
      key = "{" + raw_key + (self.hold and " down" or "") + "}"
      self.program.send_keystrokes(key)
      if x != self.presses:
        time.sleep(random.uniform(self.delay[0], self.delay[1]))
      if self.hold:
        self.program.send_keystrokes("{"+raw_key+"}")
    else:
      time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)

  def get_key(self):
    return isinstance(self.key, list) and random.choice(self.key) or self.key
