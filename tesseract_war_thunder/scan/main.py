import urllib3
from models import Player
from settings import *
import re
import requests
from requests.exceptions import ConnectionError
from time import sleep

from tesseract_war_thunder.scan.services import make_dict, player_dict, return_new_lines, \
    scan_line, check_or_create

# while True:
code_dict = {
    'kill': 'сбил',
    'crashed': 'разбился'
}


def scan_enemies(frequency):
    string_set = {}
    n = 0
    while True:
        sleep(frequency)
        new_lines = None
        n += 1
        try:
            resp_chat = requests.get('http://desktop-qt0sfna:8111/', params={'lastEvt': 0, 'lastDmg': 0})
            print(resp_chat.text)
        except requests.exceptions.ConnectionError:
            print('No connection')
        else:
            resp_dict = make_dict(resp_chat.text).get('damage')
            # if n > 2:
            #     resp_dict.append({'id': 101, 'msg': 'Абрамович (J21A-1) разбился', 'sender': '', 'enemy': False, 'mode': ''})
            # if n > 4:
            #     resp_dict.append({'id': 102, 'msg': 'CapScraffingiu (A-26B-10) разбился', 'sender': '', 'enemy': False, 'mode': ''})
            new_lines = return_new_lines(resp_dict, string_set)
        if new_lines:

            for value in new_lines.values():
                scanned_line = scan_line(value)
                if scanned_line is not None:
                    action = scanned_line['action']
                    attacker_name = scanned_line['aggressive_name']
                    attacker_plane = scanned_line['aggressive_transport']
                    victim_name = scanned_line['victim_name']
                    victim_plane = scanned_line['victim_transport']
                    attacker = check_or_create(attacker_name, attacker_plane)
                    victim = check_or_create(victim_name, victim_plane)

                    if action == 'kill':
                        victim.die()
                    elif action == 'damaged' or action == 'arson':
                        victim.damage_transport()
                    elif action == 'crashed':
                        attacker.die()
            for i in player_dict.values():
                if i.live and i.player_name is not None and i.player_name != 'AI':
                    print(i.player_name, i.player_transport)
            print('-----------------')


scan_enemies(0.5)



