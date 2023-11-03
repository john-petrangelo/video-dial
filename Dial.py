import rotaryio
import board
import keypad

import usb_hid
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import time

### CONFIGURATION

# GPIO pin assignements
mic_gp = board.GP9
cam_gp = board.GP2
mode_gp = board.GP6

# Keypad indices
mic_key = 0
cam_key = 1
mode_key = 2

# Modes (Teams or Zoom)
# The default mode is Zoom - if switch is in Teams position then we'll get a "pressed" event on startup
mode_teams = "Teams"
mode_zoom = "Zoom"
mode = mode_zoom


def toggle_mic():
    print("toggling mic")
    if mode == mode_teams:
        #kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.M)
        kbd.send(Keycode.SHIFT, Keycode.M)
    else:
        #kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.A)
        kbd.send(Keycode.SHIFT, Keycode.A)


def toggle_cam():
    print("toggling cam")
    if mode == mode_teams:
        #kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.O)
        kbd.send(Keycode.SHIFT, Keycode.O)
    else:
        #kbd.send(Keycode.COMMAND, Keycode.SHIFT, Keycode.V)
        kbd.send(Keycode.SHIFT, Keycode.V)


### MAIN PROGRAM


print("Dial starting up")
print(f"Setting mode to {mode}")

# Setup the USB HID devices
consumer_control = ConsumerControl(usb_hid.devices)
kbd = Keyboard(usb_hid.devices)

rot_enc = rotaryio.IncrementalEncoder(board.GP20, board.GP21, 2)
last_position = 0

keys = keypad.Keys((mic_gp, cam_gp, mode_gp), value_when_pressed=False, pull=True, interval=0.100)

while True:
    # Handle changes to the rotary encoder
    new_position = rot_enc.position
    if new_position > last_position:
        print(f"volume up ({new_position})")
        consumer_control.send(ConsumerControlCode.VOLUME_INCREMENT)
    if new_position < last_position:
        print(f"volume down ({new_position})")
        consumer_control.send(ConsumerControlCode.VOLUME_DECREMENT)
    last_position = new_position
    
    # Handle button presses and switch toggles
    event = keys.events.get()
    if event:
        if event.key_number == mic_key and event.pressed:
            toggle_mic()
        if event.key_number == cam_key and event.pressed:
            toggle_cam()
        if event.key_number == mode_key:
            mode = mode_teams if event.pressed else mode_zoom
            print(f"Setting mode to {mode}")
