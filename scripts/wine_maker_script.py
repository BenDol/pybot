# system
import random
import time
from enum import Enum

# core
from script import Script
from tasks import task
from tasks import TaskHandler

#util
import util.color as color

class State(Enum):
  Off = 0
  OpenBag = 1
  OpenBank = 2
  DepositItems = 3
  WithdrawItems = 4
  CloseBank = 5
  UseItems = 6
  WaitForItems = 7

class WineMakerScript(Script):
  def __init__(self, parent, config):
    super().__init__(parent, config, __name__)
    self.state = State.OpenBag
    self.bag_open = False
    self.bank_open = False
    self.deposited = False
    self.withdrawn = False
    self.used_items = False
    self.items_mixed = False

  def load(self, conf):
    super().load(conf)

  def unload(self):
    super().unload()

  def start(self):
    super().start()

  def sync(self):
    if not self.game.screen_capture:
      return False

    pixel = self.game.screen_capture.getpixel((1358, 1123))
    self.bank_open = color.is_match(pixel, [38, 250, 43], 10)

    if self.bank_open:
      self.bag_open = self.bank_open
    else:
      pixel = self.game.screen_capture.getpixel((2324, 904))
      self.bag_open = color.is_match(pixel, [111, 37, 28], 10)
    return True

  @task(delay=[0.4,0.9], silent=True)
  def state_update(self, *args):
    self.sync()

    match self.state:
      case State.OpenBag:
        if self.bag_open:
          self.state = State.OpenBank
      case State.OpenBank:
        if self.bank_open:
          self.deposited = False
          self.state = State.DepositItems
      case State.DepositItems:
        if self.deposited:
          self.withdrawn = False
          self.state = State.WithdrawItems
      case State.WithdrawItems:
        if self.withdrawn:
          self.state = State.CloseBank
      case State.CloseBank:
        if not self.bank_open:
          self.used_items = False
          self.state = State.UseItems
      case State.UseItems:
        if self.used_items:
          self.items_mixed = False
          self.state = State.WaitForItems
      case State.WaitForItems:
        if self.items_mixed:
          self.state = State.OpenBag
      case _:
        pass
    #self.run_task(self.check_bag)

  @task(delay=[1,3], silent=True)
  def open_bag(self, *args):
    self.sync()
    if self.bank_open:
      self.bag_open = True
      return False

    def can_start():
      self.sync()
      return not self.bank_open and not self.bag_open
    def started():
      print("started open_bag")
    def completed():
      print("completed open_bag")
      pixel = self.game.screen_capture.getpixel((2324, 904))
      self.bag_open = color.is_match(pixel, [111, 37, 28], 10)
    def failed(err):
      print("failed")
    return TaskHandler(can_start=can_start, started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def open_bank(self, *args):
    if self.state != State.OpenBank:
      return False

    def can_start():
      print("can_start open_bank")
      pixel = self.game.screen_capture.getpixel((1358, 1123))
      self.bank_open = color.is_match(pixel, [38, 250, 43], 10)
      return not self.bank_open
    def started():
      print("started open_bank")
    def completed():
      print("completed open_bank")
      pixel = self.game.screen_capture.getpixel((1358, 1123))
      self.bank_open = color.is_match(pixel, [38, 250, 43], 10)
    def failed(err):
      print("failed")
    return TaskHandler(can_start=can_start, started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def deposit_items(self, *args):
    if self.state != State.DepositItems:
      return False

    def started():
      print("started deposit_items")
    def completed():
      print("completed deposit_items")
      self.deposited = True
    def failed(err):
      print("failed")
    return TaskHandler(started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def withdraw_items(self, *args):
    if self.state != State.WithdrawItems:
      return False

    def started():
      print("started withdraw_items")
    def completed():
      print("completed withdraw_items")
      self.withdrawn = True
    def failed(err):
      print("failed")
    return TaskHandler(started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def close_bank(self, *args):
    if self.state != State.CloseBank:
      return False

    def can_start():
      print("can_start close_bank")
      pixel = self.game.screen_capture.getpixel((1358, 1123))
      self.bank_open = color.is_match(pixel, [38, 250, 43], 10)
      print(self.bank_open)
      return self.bank_open
    def started():
      print("started close_bank")
    def completed():
      print("completed close_bank")
      pixel = self.game.screen_capture.getpixel((1358, 1123))
      self.bank_open = color.is_match(pixel, [38, 250, 43], 10)
    def failed(err):
      print("failed")
    return TaskHandler(started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def use_items(self, *args):
    if self.state != State.UseItems:
      return False

    print(self.state)

    def started():
      print("started use_items")
    def completed():
      print("completed use_items")
      self.used_items = True
    def failed(err):
      print("failed")

    return TaskHandler(started=started, completed=completed, failed=failed)

  @task(delay=[1,3], silent=True)
  def wait_for_items(self, *args):
    if self.state != State.WaitForItems:
      return False

    def started():
      print("started wait_for_items")
    def completed():
      print("completed wait_for_items")
      pixel = self.game.screen_capture.getpixel((2310, 1139))
      self.items_mixed = color.is_match(pixel, [159, 51, 44], 5)
    def failed(err):
      print("failed")
    return TaskHandler(started=started, completed=completed, failed=failed)