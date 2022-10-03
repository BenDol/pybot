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

from win32gui import GetWindowText, GetForegroundWindow

import win32gui
import win32ui
from ctypes import windll
from PIL import Image

def window_current():
  return GetWindowText(GetForegroundWindow())

def capture_screen(hwnd):
  if isinstance(hwnd, str):
    hwnd = win32gui.FindWindow(None, hwnd)

  # Change the line below depending on whether you want the whole window
  # or just the client area. 
  #windll.user32.SetProcessDPIAware()
  _left, _top, _right, _bot = win32gui.GetClientRect(hwnd)
  left, top = win32gui.ClientToScreen(hwnd, (_left, _top))
  right, bot = win32gui.ClientToScreen(hwnd, (_right, _bot))
  #left, top, right, bot = win32gui.GetWindowRect(hwnd)
  w = right - left
  h = bot - top

  hwndDC = win32gui.GetWindowDC(hwnd)
  mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
  saveDC = mfcDC.CreateCompatibleDC()

  saveBitMap = win32ui.CreateBitmap()
  saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

  saveDC.SelectObject(saveBitMap)

  # Change the line below depending on whether you want the whole window
  # or just the client area. 
  result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
  #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 0)

  bmpinfo = saveBitMap.GetInfo()
  bmpstr = saveBitMap.GetBitmapBits(True)

  im = Image.frombuffer(
      'RGB',
      (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
      bmpstr, 'raw', 'BGRX', 0, 1)

  win32gui.DeleteObject(saveBitMap.GetHandle())
  saveDC.DeleteDC()
  mfcDC.DeleteDC()
  win32gui.ReleaseDC(hwnd, hwndDC)

  #if result == 1:
      #PrintWindow Succeeded
  #    im.save("test.png")

  return im, result
