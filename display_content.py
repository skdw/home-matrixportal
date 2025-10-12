# Content to be displayed on the RGB matrix

# Adafruit display libraries
import terminalio
import adafruit_display_text.label

colors = {
    "RED": 0xff0000,
    "RED1": 0xaa0000,
    "RED2": 0x880000,
    "RED3": 0x440000,
    "ORANGE": 0xffaa00,
    "ORANGE1": 0xaa4400,
    "ORANGE2": 0x884400,
    "ORANGE3": 0x444400,
    "YELLOW": 0xffff00,
    "GREEN": 0x00ff00,
    "GREEN1": 0x00aa00,
    "GREEN2": 0x008800,
    "GREEN3": 0x004400,
    "BLUE": 0x0000ff,
    "BLUE1": 0x0000aa,
    "BLUE2": 0x000088,
    "BLUE3": 0x000044,
    "PURPLE": 0xff00ff,
    "PURPLE1": 0xaa00aa,
    "PURPLE2": 0x880088,
    "PURPLE3": 0x440044,
    "WHITE": 0xffffff,
}

line0 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=colors["RED1"],
    text="Skynet Board")
line0.x = 0
line0.y = 8

line1 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=colors["ORANGE1"],
    text="")
line1.x = 0
line1.y = 20

line2 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=colors["ORANGE1"],
    text="")
line2.x = 0
line2.y = 32

line3 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=colors["ORANGE1"],
    text="")
line3.x = 0
line3.y = 44

line4 = adafruit_display_text.label.Label(
    terminalio.FONT,
    color=colors["RED1"],
    text="")
line4.x = 0
line4.y = 56

lines = [line0, line1, line2, line3, line4]
