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
    pixel = self.program.screen_capture.getpixel((self.pixel_pos[0], self.pixel_pos[1]))
    print(pixel)
    if not color.is_match(pixel, self.pixel_color, self.pixel_tolerance) or self.pixel_mismatch:
      super().update(task)

  def post_update(self, task):
    super().post_update(task)
