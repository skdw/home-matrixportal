# code.py
# 
# MatrixPortal Home Assistant Display
# -----------------------------------
# This module connects an Adafruit MatrixPortal to Wi-Fi and Home Assistant via MQTT,
# subscribes to events, and displays messages on an RGB matrix. It uses a custom
# character map for extended character support and handles display updates.


# Standard library
import asyncio
from os import getenv

# Adafruit networking & MQTT
import wifi
import adafruit_connection_manager
import adafruit_minimqtt.adafruit_minimqtt as MQTT

# Adafruit display libraries
import board
import displayio
import framebufferio
import rgbmatrix
import terminalio
import adafruit_display_text.label

# Character map for extended character support
# Note: unicodedata is not available on Adafruit boards
try:
    import character_map
    print("Character map loaded successfully.")
except ImportError:
    print("ERROR: character_map.py not found.")
    print("Please create it with the PC script and copy it to the CIRCUITPY drive.")
    # Stop the code if the map is missing
    while True:
        pass

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=128, height=64, bit_depth=2,
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
        board.MTX_ADDRD,
        board.MTX_ADDRE
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE
)
display = framebufferio.FramebufferDisplay(matrix, rotation=0)

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

#### Wi-Fi ###

ssid = getenv("CIRCUITPY_WIFI_SSID")
password = getenv("CIRCUITPY_WIFI_PASSWORD")

print(f"Connecting to {ssid}")
wifi.radio.connect(ssid, password)
print(f"Connected to {ssid}!")

### MQTT Feed ###
mqtt_feed = getenv("MQTT_FEED")

# Define callback methods which are called when events occur
def connected(client, userdata, flags, rc):
    # This function will be called when the client is connected
    # successfully to the broker.
    print(f"Connected to IO! Listening for topic changes on {mqtt_feed}")
    # Subscribe to all changes on the MQTT feed.
    client.subscribe(mqtt_feed)


def disconnected(client, userdata, rc):
    # This method is called when the client is disconnected
    print("Disconnected from IO!")


def message(client, topic, message):
    # This method is called when a topic the client is subscribed to
    # has a new message.
    print(f"New message on topic {topic}: {message}")
    message_chars = []
    for char in message:
        message_chars.append(character_map.ACCENT_MAP.get(char, char))
    message = "".join(message_chars)

    topic_leaf = topic.rsplit('/', 1)[-1]
    if topic_leaf == 'line_0':
        line0.text = message
    if topic_leaf == 'line_1':
        line1.text = message
    if topic_leaf == 'line_2':
        line2.text = message
    if topic_leaf == 'line_3':
        line3.text = message
    if topic_leaf == 'line_4':
        line4.text = message

# Create a socket pool and ssl_context
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)

# Set up a MiniMQTT Client
mqtt_client = MQTT.MQTT(
    broker=getenv("MQTT_BROKER"),
    username=getenv("MQTT_USERNAME"),
    password=getenv("MQTT_PASSWORD"),
    socket_pool=pool,
    ssl_context=ssl_context,
    socket_timeout=1
)

# Setup the callback methods above
mqtt_client.on_connect = connected
mqtt_client.on_disconnect = disconnected
mqtt_client.on_message = message

# Connect the client to the MQTT broker.
# print("Connecting to IO...")
# mqtt_client.connect()

async def mqtt_loop():
    print("Connecting to MQTT...")
    mqtt_client.connect()
    while True:        
        try:
            # Poll the message queue
            mqtt_client.loop(timeout=1)
        except Exception as e:
            print(f"MQTT Error: {e}. Reconnecting...")
        # mqtt_client.loop()  # Check for messages
        # await asyncio.sleep(0.1)  # Let other tasks run

########


# Put each line of text into a Group, then show that group.
g = displayio.Group()
g.append(line0)
g.append(line1)
g.append(line2)
g.append(line3)
g.append(line4)
display.root_group = g

# bitmap = displayio.Bitmap(display.width, display.height, 256)

# # This function will scoot one label a pixel to the left and send it back to
# # the far right if it's gone all the way off screen. This goes in a function
# # because we'll do exactly the same thing with line1 and line2 below.
# def scroll(line):
#     line.x = line.x - 1
#     line_width = line.bounding_box[2]
#     if line.x < -line_width:
#         line.x = display.width

# # This function scrolls lines backwards.  Try switching which function is
# # called for line2 below!
# def reverse_scroll(line):
#     line.x = line.x + 1
#     line_width = line.bounding_box[2]
#     if line.x >= display.width:
#         line.x = -line_width

# You can add more effects in this loop. For instance, maybe you want to set the
# color of each label to a different value.

async def display_loop():
    while True:
        # scroll(line1)
        display.refresh(minimum_frames_per_second=30) # 60

async def main():
    await asyncio.gather(
        mqtt_loop(),
        display_loop()
    )

asyncio.run(main())
