import win32api
import pywinauto

import random
import time

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

  def navigate(self, xy, step=1, delay=None, callback=None):
    sx, sy = self.get_xy()
    tx, ty = xy

    modx = sx < tx and step or -step
    mody = sy < ty and step or -step

    for x in range(sx, tx, modx):
      for y in range(sy, ty, mody):
        self.move(xy=(x, y), delay=delay)
        x += modx

    if callback:
      callback(self, xy)


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