from adafruit_display_shapes.rect import Rect

class Pawn:
    color = 0x444444

    def __init__(self, x=1, y=1):
        self.x = x
        self.y = y
        self.view = Rect(x, y, 1, 1, fill=self.color)

    def show(self, group):
        group.append(self.view)

    def move(self, x, y):
        self.x = x
        self.y = y
        self.update_view()

    def update_view(self):
        self.view.x = self.x
        self.view.y = self.y