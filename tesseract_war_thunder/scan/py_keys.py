from threading import Thread

from pynput import keyboard

# The currently active modifiers
# from tesseract_war_thunder.scan.main import scan_enemies
# from tesseract_war_thunder.scan.settings import frequency
# from tesseract_war_thunder.scan.tesseract_scan import make_players_dict
from tesseract_war_thunder.scan.crowler import crowl_list
from tesseract_war_thunder.scan.main import scan_enemies
from tesseract_war_thunder.scan.services import check_enemy
from tesseract_war_thunder.scan.settings import frequency
from tesseract_war_thunder.scan.tesseract_scan import make_players_dict

current = set()
# The key combination to check
COMBINATIONS = [
    {keyboard.Key.shift, keyboard.KeyCode(char='p')},
    {keyboard.Key.shift, keyboard.KeyCode(char='P')},
    {keyboard.Key.shift, keyboard.KeyCode(char='з')},
    {keyboard.Key.shift, keyboard.KeyCode(char='З')}
]
Thread(target=crowl_list).start()
make_players_dict()
# Thread(target=check_enemy).start()
scan_enemies(frequency)


def execute():
    print("Make screenshot")
    # Thread(target=crowl_list).start()
    # make_players_dict()
    # Thread(target=check_enemy).start()
    # scan_enemies(frequency)


def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()


def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)


with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()

# scan_enemies(frequency)
