"""Read in attempts from a keyboard-like magstripe reader."""
import logging
import time

from evdev import InputDevice, categorize, ecodes

SCANCODES = {
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

CAPSCODES = {
    0: None, 1: u'ESC', 2: u'!', 3: u'@', 4: u'#', 5: u'$', 6: u'%', 7: u'^', 8: u'&', 9: u'*',
    10: u'(', 11: u')', 12: u'_', 13: u'+', 14: u'BKSP', 15: u'TAB', 16: u'Q', 17: u'W', 18: u'E', 19: u'R',
    20: u'T', 21: u'Y', 22: u'U', 23: u'I', 24: u'O', 25: u'P', 26: u'{', 27: u'}', 28: u'CRLF', 29: u'LCTRL',
    30: u'A', 31: u'S', 32: u'D', 33: u'F', 34: u'G', 35: u'H', 36: u'J', 37: u'K', 38: u'L', 39: u':',
    40: u'\'', 41: u'~', 42: u'LSHFT', 43: u'|', 44: u'Z', 45: u'X', 46: u'C', 47: u'V', 48: u'B', 49: u'N',
    50: u'M', 51: u'<', 52: u'>', 53: u'?', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
    }

class EntryAttemptInterface(object):
  """Represents an input device"""
  def __init__(self, device_name="/dev/input/event0"):
    self.reader = InputDevice(device_name)

  def getAttempt(self):
    """Block on getting one entry attempt"""

    # Evdev code borrowed heavily from http://stackoverflow.com/a/19757397

    # TODO: What do we do if we can't grab the reader? Can we ungrab it first?
    # What do we do if some part of the reading fails? Ungrabbing should occur regardless,
    # but how?

    # Wait until we can access the devicde
    grabbed = False
    while not grabbed:
      try:
        self.reader.grab()
        grabbed = True
      except IOError:
        time.sleep(0.1)

    caps = False
    result = u''

    for event in self.reader.read_loop():
      if event.type == ecodes.EV_KEY:
        data = categorize(event)
        if data.scancode == 28 and data.keystate == 1: # Enter key presed
          break

        if data.scancode == 42 or data.scancode == 54: # Shift key pressed or unpressed

          if data.keystate == 1:
            caps = True
          else:
            caps = False 

        elif data.keystate == 1:

          key_lookup = ((CAPSCODES if caps else SCANCODES).get(data.scancode)
              or u'UNKNOWN:[{}]'.format(data.scancode))
          result += key_lookup

    self.reader.ungrab()

    return result

