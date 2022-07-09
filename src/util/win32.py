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
