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

# Character map for extended character support
# Note: unicodedata is not available on Adafruit boards
import character_map

# Custom display content module
import display_content

displayio.release_displays()
matrix = rgbmatrix.RGBMatrix(
    width=256, height=64, bit_depth=2,
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

    # Replace accented characters
    message_chars = []
    for char in message:
        message_chars.append(character_map.ACCENT_MAP.get(char, char))
    message_noaccent = "".join(message_chars)

    topic_leafs = topic.rsplit('/', 2)
    if topic_leafs[-2] == 'text':
        # Update the appropriate line text based on the topic
        line_no = int(topic_leafs[-1])
        print(f"Updating line {line_no} to: {message_noaccent}")
        display_content.lines[line_no].text = message_noaccent
    if topic_leafs[-2] == 'color':
        # Update the appropriate line color based on the topic
        line_no = int(topic_leafs[-1])
        print(f"Updating line {line_no} color to: {message}")
        if message in display_content.colors:
            display_content.lines[line_no].color = display_content.colors[message]
        else:
            print(f"Color {message} not found in colors dictionary.")

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
for line in display_content.lines:
    g.append(line)
display.root_group = g

# bitmap = displayio.Bitmap(display.width, display.height, 256)

async def display_loop():
    while True:
        display.refresh(minimum_frames_per_second=30) # 60

async def main():
    await asyncio.gather(
        mqtt_loop(),
        display_loop()
    )

asyncio.run(main())
