import displayio
from Stack import Stack
import os


def get_random(start, stop):
    return int.from_bytes(os.urandom(2), "big") % stop + start


def array_shuffle(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = get_random(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr


class Maze:
    def is_META(self, x, y):
        return self.bitmap[x, y] == 3

    def is_wall(self, x, y):
        return self.bitmap[x, y] == 1 or self.bitmap[x, y] == 2

    def is_border(self, x, y):
        if x == 0 or x == self.WIDTH - 1:
            return True
        if y == 0 or y == self.HEIGHT - 1:
            return True
        return False

    def is_in(self, x, y):
        if x < 0 or x >= self.WIDTH:
            return False
        if y < 0 or y >= self.HEIGHT:
            return False
        return True

    def only_one_visited(self, x, y, v):
        c = 0
        for xx, yy in v:
            if self.is_in(x + xx, y + yy):
                if self.bitmap[x + xx, y + yy] == 0:
                    c += 1
        return c <= 1

    def make_border(self):
        for i in range(self.WIDTH):
            self.bitmap[i, 0] = 1
            self.bitmap[i, self.HEIGHT - 1] = 1
        for i in range(1, self.HEIGHT - 1):
            self.bitmap[0, i] = 1
            self.bitmap[self.WIDTH - 1, i] = 1

    def pair_to_index(self, x, y):
        return x + self.WIDTH * y

    def index_to_pair(self, index):
        return (index % self.WIDTH, index // self.WIDTH)

    def is_visited(self, x, y):
        return self.bitmap[self.pair_to_index(x, y)] != 2

    def generate(self, START):
        v = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        self.bitmap.fill(2)
        self.make_border()
        stack = Stack()
        stack.push(self.pair_to_index(START[0], START[1]))
        while not stack.is_empty():
            index = stack.pop()
            x, y = self.index_to_pair(index)
            if self.only_one_visited(x, y, v):
                self.bitmap[index] = 0
                array_shuffle(v)
                for xx, yy in v:
                    if (
                        self.is_in(x + xx, y + yy)
                        and not self.is_border(x + xx, y + yy)
                        and not self.is_visited(x + xx, y + yy)
                    ):
                        stack.push(self.pair_to_index(x + xx, y + yy))
                        self.bitmap[x + xx, y + yy] = 1
            else:
                self.bitmap[index] = 1

    def place_META(self):
        def get_distance(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        max_dist = -1
        META = None
        for i in range(1, self.WIDTH):
            for j in range(1, self.HEIGHT):
                if not self.is_wall(i, j):
                    dist = get_distance(self.START, (i, j))
                    if dist > max_dist:
                        max_dist = dist
                        META = (i, j)
        return META

    def __init__(self, w, h):
        self.WIDTH = w
        self.HEIGHT = h
        self.NUM_OF_CELLS = self.WIDTH * self.HEIGHT
        self.bitmap = displayio.Bitmap(self.WIDTH, self.HEIGHT, 4)
        clrPallete = displayio.Palette(4)
        clrPallete[0] = (0, 0, 0) # path
        clrPallete[1] = (70, 0, 0) # wall
        clrPallete[2] = (70, 0, 0) # unvisited
        clrPallete[3] = 0x00FF00  # META
        self.START = (1, 1)
        self.grid = displayio.TileGrid(self.bitmap, pixel_shader=clrPallete)

    def show(self, group):
        group.append(self.grid)
        self.generate(self.START)
        self.META = self.place_META()
        self.bitmap[self.META[0], self.META[1]] = 3
