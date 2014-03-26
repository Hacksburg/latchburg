"""Utilities for dealing with latches' actuators in the physical universe."""

import threading
import time

import RPi.GPIO as GPIO

LOCK_PIN = 6
LOCKLOCK = threading.RLock()


GPIO.setmode(GPIO.BOARD)
GPIO.setup(LOCK_PIN, GPIO.OUT)
GPIO.output(LOCK_PIN, GPIO.LOW)

def unlock(open_period):
  """Open the latch for `open_period` seconds.

  Doesn't block: Opens a thread to hold the latch open for the specified
  period of time. If this is called while the latch is being held open, this
  effectively will do nothing. It will not modify the length of time the latch
  is held, nor raise an exception nor fail in any other way."""

  def open_sesame():
    if LOCKLOCK.acquire(blocking=False):
      GPIO.output(6, GPIO.HIGH)
      time.sleep(open_period)
      GPIO.output(6, GPIO.LOW)
      LOCKLOCK.release()

  threading.Thread(target=open_sesame).start()
