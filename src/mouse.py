import win32api
import pywinauto

import random
import time
import math

class Mouse(object):
  def __init__(self, engine, config):
    self.engine = engine
    self.config = config

  def get_xy(self):
    pass

  def move(self, xy, delay=None):
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))

  def click(self, button, delay=None):
    if delay:
      time.sleep(random.uniform(delay[0], delay[1]))

  def navigate(self, xy, speed=[100, 200], delay=None, callback=None):
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
      callback(self, xy)

  def range(self, range):
    return random.randint(range[0], range[1])


class PyWinMouse(Mouse):
  def __init__(self, config):
    super().__init__(pywinauto.mouse, config)

  def get_xy(self):
    return win32api.GetCursorPos()

  def move(self, xy, delay=None):
    super().move(xy, delay)
    self.engine.move(coords=xy)

  def click(self, button='left', delay=None):
    super().click(button, delay)
    self.engine.click(button=button, coords=self.get_xy())