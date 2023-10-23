import time
import rotaryio
import board
import digitalio
import keypad


##### Keypad info

#keys = keypad.Keys((board.D5,), value_when_pressed=False, pull=True, interval=0.020)

#while True:
#    event = keys.events.get()
#    # event will be None if nothing has happened.
#    if event:
#        print(event)
#        event.key_number - keys are numbered starting at 0
#        event.pressed
#        event.released


def setup_button(pin):
    button = digitalio.DigitalInOut(pin)
    button.direction = digitalio.Direction.INPUT
    button.pull = digitalio.Pull.UP
    return button
    

def print_state():
        print(f"Volume={new_volume} Mic={new_mic_state:1}  Cam={new_cam_state:1}  Mode={new_mode_state:1}")


# MAIN PROGRAM

print("Dial starting up")

rot_enc = rotaryio.IncrementalEncoder(board.GP20, board.GP21, 2)
last_volume = 0

cam_button = setup_button(board.GP2)
last_cam_state = None

mic_button = setup_button(board.GP13)
last_mic_state = None

mode_switch = setup_button(board.GP9)
last_mode_state = None

while True:
    new_volume = rot_enc.position
    if new_volume >= last_volume:
        # Volume up
        pass
    if new_volume <= last_volume:
        # Volume down
        pass
    
    new_cam_state = not cam_button.value
    if last_cam_state is None or new_cam_state != last_cam_state:
        # Camera on/off button pressed

        # Poor man's debounce
        time.sleep(0.1)
    
    new_mic_state = not mic_button.value
    if last_mic_state is None or new_mic_state != last_mic_state:
        # Microphone on/off button pressed

        # Poor man's debounce
        time.sleep(0.1)
    
    new_mode_state = not mode_switch.value
    if last_mode_state is None or new_mode_state != last_mode_state:
        # Mode switch switched

        # Poor man's debounce
        time.sleep(0.1)

    if [last_volume, last_cam_state, last_mic_state, last_mode_state] != [new_volume, new_cam_state, new_mic_state, new_mode_state]:
        print_state()

        # Save all of the new states
        last_volume = new_volume
        last_mic_state = new_mic_state
        last_cam_state = new_cam_state
        last_mode_state = new_mode_state

