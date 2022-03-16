import json
import pandas
import urllib3
from models import Player
from settings import *
import re
import requests
from requests.exceptions import ConnectionError
from time import sleep

from tesseract_war_thunder.scan.services import player_dict, return_new_lines, \
    scan_line, check_or_create


def scan_enemies(frequency):
    string_set = {}
    n = 0
    while True:
        sleep(frequency)
        new_lines = None
        n += 1
        try:
            resp_chat = requests.get('http://localhost:8111/hudmsg', params={'lastEvt': 0, 'lastDmg': 500})
            # with open('data.txt', 'w') as outfile:
            #     json.dump(resp_chat.text, outfile)
            # with open('data.txt', 'r') as file:
            #     resp_chat = json.load(file)

        except requests.exceptions.ConnectionError:
            print('No connection')
        else:
            resp_dict = json.loads(resp_chat.text).get('damage')
            new_lines = return_new_lines(resp_dict, string_set)
        if new_lines:

            for value in new_lines.values():
                parsed_dict = scan_line(value)
                if parsed_dict is not None:
                    action = parsed_dict['action']
                    attacker = check_or_create(parsed_dict['aggressive_info'])
                    victim = check_or_create(parsed_dict['victim_info'])

                    if action == 'kill':
                        victim.die()
                    elif action == 'damaged' or action == 'arson':
                        victim.damage_transport()
                    elif action == 'crashed':
                        attacker.die()
            for i in player_dict.values():
                if i.live and i.player_name is not None and i.player_name != 'AI':
                    stats = i.stats['Реалистичный режим'] if isinstance(i.stats, dict) else ''
                    if i.enemy:

                        print(str(i) + ' ' + str(i.enemy), stats)
            print('-----------------')


scan_enemies(frequency)


