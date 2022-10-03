# MIT License
# 
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

import win32api
import pywinauto

import random
import time
import math

from pywinauto.timings import Timings

Timings.fast()
Timings._timings['after_clickinput_wait'] = 0
Timings._timings['after_setcursorpos_wait'] = 0

class Mouse(object):
  def __init__(self, engine, config):
    self.engine = engine
    self.config = config
    self.locked = False

  def get_xy(self):
    pass

  def move(self, xy, delay=None):
    if self.locked:
      raise RuntimeError("Mouse locked")

    self.lock()
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))
    return True

  def click(self, button, delay=None):
    if self.locked:
      raise RuntimeError("Mouse locked")

    self.lock()
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))
    return True

  def navigate(self, xy, speed=[25, 55], delay=None, callback=None):
    if self.locked:
      raise RuntimeError("Mouse locked")

    tx, ty = xy
    x, y = self.get_xy()

    while x != tx or y != ty:
      dirx = tx-x
      diry = ty-y

      mag = math.sqrt(dirx * dirx + diry * diry)

      cx = math.floor((dirx / mag) * self.range(speed))
      cy = math.floor((diry / mag) * self.range(speed))

      x += cx
      y += cy

      # normalize
      x = cx >= 0 and min(tx, x) or max(tx, x)
      y = cy >= 0 and min(ty, y) or max(ty, y)

      self.move(xy=(x, y), delay=delay)

    if callback:
      return callback(self, xy)

    return True

  def range(self, range):
    return random.randint(range[0], range[1])

  def lock(self):
    self.locked = True

  def unlock(self):
    self.locked = False


class PyWinMouse(Mouse):
  def __init__(self, config):
    super().__init__(pywinauto.mouse, config)

  def get_xy(self):
    return win32api.GetCursorPos()

  def move(self, xy, delay=None):
    if super().move(xy, delay):
      self.engine.move(coords=xy)
      self.unlock()
      return True

  def click(self, button='left', delay=None):
    if super().click(button, delay):
      self.engine.click(button=button, coords=self.get_xy())
      self.unlock()
      return True
