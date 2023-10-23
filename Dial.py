import rotaryio
import board
import keypad


# CONFIGURATION

mic_gp = board.GP13
cam_gp = board.GP2
mode_gp = board.GP9

mic_key = 0
cam_key = 1
mode_key = 2

mode_teams = 1
mode_zoom = 0

# default mode is Zoom - if switch is in Teams position then we'll get a "pressed" event on startup
mode = mode_zoom

# MAIN PROGRAM

print("Dial starting up")

rot_enc = rotaryio.IncrementalEncoder(board.GP20, board.GP21, 2)
last_volume = 0

keys = keypad.Keys((mic_gp, cam_gp, mode_gp), value_when_pressed=False, pull=True, interval=0.100)

while True:
    new_volume = rot_enc.position
    if new_volume > last_volume:
        print(f"volume up ({new_volume})")
    if new_volume < last_volume:
        print(f"volume down ({new_volume})")
    last_volume = new_volume
    
    event = keys.events.get()
    if event:
        if event.key_number == mic_key and event.pressed:
            print("mic pressed")
        if event.key_number == cam_key and event.pressed:
            print("cam pressed")
        if event.key_number == mode_key and event.pressed:
            print("mode=Teams")
        if event.key_number == mode_key and event.released:
            print("mode=Zoom")
