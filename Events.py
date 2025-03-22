from digitalio import DigitalInOut, Direction, Pull
import adafruit_lis3dh
import board
import busio
from Loop import loop
import time
import microcontroller

class _Events:
    SENSOR = 0
    UP = 1
    DOWN = 2
    def __del__(self):
        loop.remove(self.task)

    def __init__(self):
        #setup sensor
        try:
            i2c = board.I2C()  # uses board.SCL and board.SDA
        except:
            microcontroller.reset()
        self.lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
        self.lis3dh.range = adafruit_lis3dh.RANGE_2_G

        self.btn_up = DigitalInOut(board.BUTTON_UP)
        self.btn_up.direction = Direction.INPUT
        self.btn_up.pull = Pull.UP

        self.btn_down = DigitalInOut(board.BUTTON_DOWN)
        self.btn_down.direction = Direction.INPUT
        self.btn_down.pull = Pull.UP

        self.NUM_TASKS = 3
        self.tasks = [ [] for _ in range(self.NUM_TASKS) ]
        self.task = self.loop
        loop.add(self.task)
    def run_tasks(self, event_id):
        for task in self.tasks[event_id]:
            task()
    def on_event(self, event_id, task):
        self.tasks[event_id].append(task)
    def on_event_remove(self, event_id, task):
        self.tasks[event_id].remove(task)
    def clean(self):
        self.tasks = [ [] for _ in range(self.NUM_TASKS) ]
    def loop(self):
        self.acc = [value / adafruit_lis3dh.STANDARD_GRAVITY for value in self.lis3dh.acceleration]

        self.run_tasks(self.SENSOR)

        if not self.btn_up.value:
            self.run_tasks(self.UP)
            time.sleep(0.5)

        if not self.btn_down.value:
            self.run_tasks(self.DOWN)
            time.sleep(0.5)

events = _Events()
