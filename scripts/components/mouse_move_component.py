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

#util
import pybot.util.vector as vector

class MouseMoveTaskComponent(TaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.position   = self.config.get("position")   or None
    self.speed      = self.config.get("speed")      or [25, 55]
    self.delay      = self.config.get("delay")      or None
    self.post_delay = self.config.get("post_delay") or [0, 0]

  def update(self, task):
    super().update(task)

    if self.position:
      if len(self.position) == 2:
        self.program.mouse.navigate(xy=(self.position[0], self.position[1]), speed=self.speed, delay=self.delay)
      else:
        self.last_pos = vector.random_point((self.position[0], self.position[1]), (self.position[2], self.position[3]))
        self.program.mouse.navigate(xy=(self.last_pos[0], self.last_pos[1]), speed=self.speed, delay=self.delay)

    time.sleep(random.uniform(self.post_delay[0], self.post_delay[1]))

  def post_update(self, task):
    super().post_update(task)
