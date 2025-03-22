import displayio
import time
from adafruit_display_text.scrolling_label import ScrollingLabel
import terminalio
from Maze import Maze
from Pawn import Pawn
from Loop import loop
from Events import events

class Game:
    def __init__(self, display, w, h):
        self.display = display
        self.WIDTH = w
        self.HEIGHT = h
        self.event = self.start
        events.on_event(events.DOWN, self.event)
        self.start()

    def close(self):
        events.on_event_remove(events.DOWN, self.event)
        loop.remove(self.task)
        self.display.root_group = None

    def can_move(self, x, y):
        if self.maze.is_wall(x, y):
            return False
        return True

    def show_finish_screen(self):
        self.text = ScrollingLabel(terminalio.FONT, text="   CO TAK WOLNO!", animate_time=0.5, max_characters=len("   CO TAK WOLNO!"))
        self.text.x = 0
        self.text.y = 14
        self.group.append(self.text)

    def update_finish_screen(self):
        self.text.update()

    def finish(self):
        self.is_end = True
        self.show_finish_screen()

    def move_pawn(self, acc):
        sens = 0.4
        if abs(acc[0]) > sens:
            sign = -1 if acc[0] < 0 else 1
            new_x = self.pawn.x + 1 * sign
            if self.can_move(new_x, self.pawn.y):
                self.pawn.move(new_x, self.pawn.y)
                time.sleep(max(1 - abs(acc[0]), 0.1))
            if self.maze.is_META(self.pawn.x, self.pawn.y):
                self.finish()
                return
        if abs(acc[1]) > sens:
            sign = -1 if acc[1] < 0 else 1
            new_y = self.pawn.y + 1 * sign
            if self.can_move(self.pawn.x, new_y):
                self.pawn.move(self.pawn.x, new_y)
                time.sleep(max(1 - abs(acc[1]), 0.1))
            if self.maze.is_META(self.pawn.x, self.pawn.y):
                self.finish()
                return

    def start(self):
        self.group = displayio.Group()
        self.display.root_group = self.group
        self.maze = Maze(self.WIDTH, self.HEIGHT)
        self.maze.show(self.group)
        self.pawn = Pawn()
        self.pawn.show(self.group)
        self.is_end = False
        self.task = self.update
        loop.add(self.task)

    def update(self):
        if not self.is_end:
            self.move_pawn(events.acc)
        else:
            self.update_finish_screen()

