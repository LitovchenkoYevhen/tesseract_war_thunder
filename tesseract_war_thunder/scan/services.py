import re

from tesseract_war_thunder.scan.models import Player

action_dict = {
    'kill': 'сбил',
    'damaged': 'подбил',
    'arson': 'поджог',
    'destroy': 'уничтожил',
    'crashed': 'разбился'
}
player_dict = {}


def make_dict(data):
    data = eval(data.replace('true', 'True').replace('false', 'False'))
    return data


def return_new_lines(data, string_set):
    new_dict = {}
    for i in data:
        id = i['id']
        msg = i['msg']
        if id not in string_set:
            string_set[id] = msg
            new_dict[id] = msg
    return new_dict


def get_name_transport_tuple(full_line: str):  # ['Fenrir_alex (␗P-47D) ', ' diezGR (A6M3)']
    line = full_line.strip()
    player_name = None
    player_transport = None
    try:
        player_transport = re.search(r'\(.+\)$', line)[0]
        player_name = re.search(r'^\W?\w+\W?\s?\w+', line)[0]
    except:
        pass
    return player_name, player_transport


def get_action_players_info(line, action):
    line = line.split(action_dict[action])
    aggressive, victim = line[0], line[1]
    aggressive_name, aggressive_transport = get_name_transport_tuple(aggressive)
    victim_name, victim_transport = get_name_transport_tuple(victim)
    result = {
        'aggressive_name': aggressive_name,
        'aggressive_transport': aggressive_transport,
        'victim_name': victim_name,
        'victim_transport': victim_transport,
        'action': action
    }
    return result


def get_pve_player(line, action):
    line = line.split(action_dict[action])
    aggressive, victim = line[0], line[1]
    aggressive_name, aggressive_transport = get_name_transport_tuple(aggressive)
    result = {
        'aggressive_name': aggressive_name,
        'aggressive_transport': aggressive_transport,
        'victim_name': 'AI',
        'victim_transport': 'AI',
        'action': action
    }
    return result


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
        result = get_pve_player(line, action)
    elif action_dict['crashed'] in line:
        action = 'crashed'
        result = get_pve_player(line, action)
    if result and action:
        return result
    return None


def check_or_create(name, plane) -> Player:
    if name not in player_dict.keys():
        player_dict[name] = Player(name, plane)
    return player_dict[name]






# z = '([^\(][а-яА-ЯёЁ]{3,})'
# reg_dict = {
#     '\([\w-]{1,9}\s?\)': ['(М-71Ф)', '(Wyvern)'],
#     '': []
# }
'\([\W\s\w-]{1,12}\)(\s+|\)|\([\w-]{1,9}\s?\){1,2})' # техника со скобками
'\s?\w+\s\([\W\s\w-]{1,12}\)(\s+|\)|\([\w-]{1,9}\s?\){1,2})' # ник + техника со скобками
'([0-9a-zA-Z])'
