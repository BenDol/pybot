from ctypes import *

MOUSE_LEFTDOWN = 0x0002
MOUSE_LEFTUP = 0x0004

MOUSE_RIGHTDOWN = 0x0008
MOUSE_RIGHTUP = 0x0010

MOUSE_MIDDLEDOWN = 0x0020
MOUSE_MIDDLEUP = 0x0040

import time
import json
import threading

from PIL import Image, ImageDraw

from util.screen import primary_screen
from util.point import Point

class MouseTracking():
  enabled = False
  thread = None
  data = []

  def draw(self):
    if len(self.data) < 1:
      return

    ps = primary_screen()
    im = Image.new('RGBA', (ps.width, ps.height), (0, 255, 0, 0)) 
    draw = ImageDraw.Draw(im)

    last_pos = {"x": self.data[0]["x"], "y": self.data[0]["y"]}
    for pos in self.data:
      lpx = last_pos["x"]
      lpy = last_pos["y"]
      px = pos["x"]
      py = pos["y"]
      #print("[" + str(lpx) + "," + str(lpy) + "] -> [" + str(px) + "," + str(py) + "]")
      draw.line((lpx,lpy, px,py), fill="#0000ff", width=4, joint='curve')
      last_pos = pos

    im.show()

mouse_tracking = MouseTracking()

def mouse_move(x, y):
  windll.user32.mouse_event(
    c_uint(0x0001),
    c_uint(x),
    c_uint(y),
    c_uint(0),
    c_uint(0)
  )

def mouse_click(button_name, hold=False):
  windll.user32.mouse_event(
    c_uint(get_mouse_button(button_name)), c_uint(0), c_uint(0), c_uint(0), c_uint(0))
  
  if not hold:
    windll.user32.mouse_event(
      c_uint(get_mouse_button(button_name, True)), c_uint(0), c_uint(0), c_uint(0), c_uint(0))

def mouse_get_button(button_name, button_up=False):
  buttons = 0
  if button_name.find("right") >= 0:
    buttons = MOUSE_RIGHTDOWN
  if button_name.find("left") >= 0:
    buttons = buttons + MOUSE_LEFTDOWN
  if button_name.find("middle") >= 0:
    buttons = buttons + MOUSE_MIDDLEDOWN
  if button_up:
    buttons = buttons << 1
  return buttons

def mouse_get_pos():
  pt = Point()
  windll.user32.GetCursorPos(byref(pt))
  return { "x": pt.x, "y": pt.y}

def mouse_track_toggle():
  global mouse_tracking
  if mouse_tracking.enabled:
    print("Mouse Tracking: Disabled")
    mouse_track_end()
  else:
    print("Mouse Tracking: Enabled")
    mouse_track_start()

def mouse_track_start():
  global mouse_tracking
  # start new thread
  # store mouse position data in array
  mouse_tracking.enabled = True
  mouse_tracking.thread = threading.Thread(target=mouse_track, args=(mouse_tracking,))
  mouse_tracking.thread.start()

def mouse_track(mouse_tracking):
  while (mouse_tracking.enabled):
    mp = mouse_get_pos()
    mouse_tracking.data.append(mp)
    print(mp)
    time.sleep(0.006)

def mouse_track_end():
  global mouse_tracking
  if not mouse_tracking.enabled:
    return
  mouse_tracking.enabled = False
  mouse_tracking.thread.join()

  # dump mouse_track_data to output as json
  path = "out/" + str(time.time()) + "_mouse_track.json"
  print("Dumping " + str(len(mouse_tracking.data)) + " tracking results to '" + path + "'")
  json_str = json.dumps(mouse_tracking.data)

  f = open(path, "w")
  f.write(json_str)
  f.close()

  mouse_tracking.data.clear()

def mouse_track_draw():
  global mouse_tracking
  mouse_tracking.draw()

