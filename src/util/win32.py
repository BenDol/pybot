from win32gui import GetWindowText, GetForegroundWindow

def window_current():
  return GetWindowText(GetForegroundWindow())
