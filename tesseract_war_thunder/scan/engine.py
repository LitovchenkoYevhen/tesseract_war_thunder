from json import dumps, loads
from time import sleep

import requests

from tesseract_war_thunder.scan.models import Scanner
from tesseract_war_thunder.scan.services import make_dict, return_new_lines

n = 0
string_set = {}

while True:
    sleep(0.5)
    new_lines = None
    n += 1
    try:
        resp_chat = Scanner('http://desktop-qt0sfna:8111/hudmsg').get_damage_list()
    except requests.exceptions.ConnectionError:
        print('No connection')
    else:
        print(resp_chat)
