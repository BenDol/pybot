# core
from pybot.core.program import Program
from pybot.core.tasks import task
from pybot.core.tasks import TaskHandler

# util
import pybot.util.color as color

class Toram(Program):
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
    super().scan(*args)
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
