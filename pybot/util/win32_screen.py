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

# Done by Frannecklp

import win32api
import win32con
import win32gui
import win32ui

import cv2
import numpy as np

def grab_screen(region=None):
  hwin = win32gui.GetDesktopWindow()

  if region:
    left, top, x2, y2 = region
    width = x2 - left + 1
    height = y2 - top + 1
  else:
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)

  hwindc = win32gui.GetWindowDC(hwin)
  srcdc = win32ui.CreateDCFromHandle(hwindc)
  memdc = srcdc.CreateCompatibleDC()
  bmp = win32ui.CreateBitmap()
  bmp.CreateCompatibleBitmap(srcdc, width, height)
  memdc.SelectObject(bmp)
  memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)

  signedIntsArray = bmp.GetBitmapBits(True)
  img = np.fromstring(signedIntsArray, dtype='uint8')
  img.shape = (height, width, 4)

  srcdc.DeleteDC()
  memdc.DeleteDC()
  win32gui.ReleaseDC(hwin, hwindc)
  win32gui.DeleteObject(bmp.GetHandle())

  return cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
