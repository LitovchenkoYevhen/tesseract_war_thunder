import re
from time import sleep

from thefuzz import process

from tesseract_war_thunder.scan.crowler import crowl_player_stats
from tesseract_war_thunder.scan.models import Player
from tesseract_war_thunder.scan.settings import action_dict, match_percent
from tesseract_war_thunder.scan.tesseract_scan import make_enemy_list

player_dict = {}


def return_new_lines(data, string_set) -> dict:
    new_dict = {}
    for i in data:
        id = i['id']
        msg = i['msg']
        if id not in string_set:
            string_set[id] = msg
            new_dict[id] = msg
    return new_dict


def get_player_info(full_line: str) -> dict:  # 'Fenrir_alex (␗P-47D) '
    line = full_line.strip()
    ai = 'AI'
    if re.search(r'\)$', line):  # Check if not AI
        player_nick = re.search(r'\s?\b\w+\b\s\(', line)[0].strip('(').strip()
        if len(player_nick) > 4:
            try:
                player_transport = re.search(r'\(.+\)', line)[0]
                player_name = re.search(r'^\W?\w+\W?\s?\w+', line)[0]
            except:
                pass
            else:
                result = {
                    'player_name': player_name,
                    'player_transport': player_transport,
                    'player_nick': player_nick
                }
                return result
    result = {
        'player_name': ai,
        'player_transport': ai,
        'player_nick': ai
    }
    return result


def get_action_players_info(line, action) -> dict:
    line = line.split(action_dict[action])
    aggressive, victim = line[0], line[1]
    aggressive_info = get_player_info(aggressive)
    victim_info = get_player_info(victim)
    result = {
        'aggressive_info': aggressive_info,
        'victim_info': victim_info,
        'action': action
    }
    return result

# todo сделать механизм установления жертвы ( это игрок или бот )
# def get_victim_info(line, action):
#     player = re.search(r'\)$', line)
#     if not player:
#         soul = False
#
#     victim_invo = {
#         'soul': soul,
#         'player_name':12
#     }
# def get_pve_player(line, action):
#     line = line.split(action_dict[action])
#     aggressive, victim = line[0], line[1]
#     aggressive_name, aggressive_transport = get_name_transport_tuple(aggressive)
#     result = {
#         'aggressive_name': aggressive_name,
#         'aggressive_transport': aggressive_transport,
#         'victim_name': 'AI',
#         'victim_transport': 'AI',
#         'action': action
#     }
#     return result


def scan_line(line: str):
    result = None
    action = None
    if action_dict['kill'] in line:
        action = 'kill'
        result = get_action_players_info(line, action)
    elif action_dict['damaged'] in line:
        action = 'damaged'
        result = get_action_players_info(line, action)
    elif action_dict['arson'] in line:
        action = 'arson'
        result = get_action_players_info(line, action)
    elif action_dict['destroy'] in line:
        action = 'destroy'
        result = get_action_players_info(line, action)
    elif action_dict['crashed'] in line:
        action = 'crashed'
        result = get_action_players_info(line, action)
    if result and action:
        return result
    return None


def check_enemy(nick):
    enemy_name_list = make_enemy_list()
    # print(type(nick))
    # print(nick, '----------', enemy_name_list)
    match_result = process.extractOne(nick, enemy_name_list)
    if match_result:
        return True
    return False


def check_or_create(parsed_dict) -> Player:
    name = parsed_dict['player_name']
    if name not in player_dict.keys():
        plane, nick = parsed_dict['player_transport'], parsed_dict['player_nick']
        # print(parsed_dict)
        enemy = check_enemy(nick)
        stats = crowl_player_stats(nick)
        player_dict[name] = Player(name, plane, nick, stats=stats, enemy=enemy)
    return player_dict[name]






# z = '([^\(][а-яА-ЯёЁ]{3,})'
# reg_dict = {
#     '\([\w-]{1,9}\s?\)': ['(М-71Ф)', '(Wyvern)'],
#     '': []
# }
'\([\W\s\w-]{1,12}\)(\s+|\)|\([\w-]{1,9}\s?\){1,2})' # техника со скобками
'\s?\w+\s\([\W\s\w-]{1,12}\)(\s+|\)|\([\w-]{1,9}\s?\){1,2})' # ник + техника со скобками
'([0-9a-zA-Z])'
