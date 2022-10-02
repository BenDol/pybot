# system
import random
import time

#util
import pybot.util.color as color

# components
from mouse_click_component import MouseClickTaskComponent

class PixelClickTaskComponent(MouseClickTaskComponent):
  def __init__(self, config):
    super().__init__(config)
    self.pixel_pos = config.get("pixel_pos") or [2324, 904]
    self.pixel_color = config.get("pixel_color") or [111, 37, 28]
    self.pixel_tolerance = config.get("pixel_tolerance") or 10
    self.pixel_mismatch = config.get("pixel_mismatch")

  def update(self, task):
    pixel = self.game.screen_capture.getpixel((self.pixel_pos[0], self.pixel_pos[1]))
    print(pixel)
    if not color.is_match(pixel, self.pixel_color, self.pixel_tolerance) or self.pixel_mismatch:
      super().update(task)

  def post_update(self, task):
    super().post_update(task)
