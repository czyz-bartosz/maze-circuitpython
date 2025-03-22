import board
import displayio
import framebufferio
import rgbmatrix
from Loop import loop
from Game import Game
from Events import events

SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32

displayio.release_displays()

matrix = rgbmatrix.RGBMatrix(
    width=64,
    bit_depth=4,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True)

game = Game(display, SCREEN_WIDTH, SCREEN_HEIGHT)

while True:
    loop.run()
