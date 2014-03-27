"""Utilities for dealing with latches' actuators in the physical universe."""

import threading
import time

import RPi.GPIO as GPIO

class Latch(object):
  """Class to deal with latches."""

  def __init__(self, lock_pin=12):
    self.lock_pin = lock_pin
    self.lock_lock = threading.RLock()


    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(lock_pin, GPIO.OUT)
    GPIO.output(lock_pin, GPIO.LOW)

  def unlock(open_period):
    """Open the latch for `open_period` seconds.

    Doesn't block: Opens a thread to hold the latch open for the specified
    period of time. If this is called while the latch is being held open, this
    effectively will do nothing. It will not modify the length of time the latch
    is held, nor raise an exception nor fail in any other way."""

    def open_sesame():
      if self.lock_lock.acquire(blocking=False):
        GPIO.output(self.lock_pin, GPIO.HIGH)
        time.sleep(open_period)
        GPIO.output(self.lock_pin, GPIO.LOW)
        self.lock_lock.release()

    threading.Thread(target=open_sesame).start()
