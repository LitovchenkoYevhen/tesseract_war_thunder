import datetime

import requests


class Player:
    player_name = None
    player_state = None
    show_player = False
    spawn_time = None

    def __init__(self, player_name=None, player_state=True, show_player=True):
        self.player_name = player_name
        self.player_state = player_state
        self.show_player = show_player

    def kill_player(self):
        self.show_player = False
        self.player_state = 'Dead'

    def spawn_player(self):
        self.show_player = True
        self.player_state = 'Alive'
        self.spawn_time = datetime.datetime.now()


class Vehicle(Player):
    vehicle_name = None
    vehicle_condition = 'Damaged'

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def destroy_transport(self):
        self.player_state = 'Dead'
        self.show_player = False
        self.vehicle_name = None


class VehicleAir(Vehicle):

    def damage_air_transport(self):
        self.vehicle_condition = 'Damaged'


class VehicleGround(Vehicle):
    pass


class Scanner:
    url = 'http://desktop-qt0sfna:8111/'
    action_dict = {
        'kill': 'сбил',
        'damaged': 'подбил',
        'arson': 'поджог',
        'destroy': 'уничтожил',
        'crashed': 'разбился'
    }

    def __init__(self, url):
        self.url = url

    def get_damage_list(self):
        damage_list = requests.get(self.url, params={'lastEvt': 0, 'lastDmg': 0}).text
        clear_dict = damage_list.replace('true', 'True').replace('false', 'False')
        eval_clear_dict = eval(clear_dict)
        damage_list = eval_clear_dict.get('damage')
        return damage_list


    @staticmethod
    def replace_js_bool(response_dict):
        return response_dict.replace('true', 'True').replace('false', 'False')



    @staticmethod
    def get_new_lines(data, string_set):
        new_dict = {}
        for i in data:
            id = i['id']
            msg = i['msg']
            if id not in string_set:
                string_set[id] = msg
                new_dict[id] = msg
        return new_dict


class Player:
    good_condition = 'not damaged'
    critical_damaged = 'has been crited'
    unknown = 'unknown'
    dead = 'dead'

    def __init__(self, player, transport, condition=good_condition):
        self.player_name = player
        self.player_transport = transport
        self.transport_condition = condition
        self.live = True

    def destroy_transport(self, unknown):
        self.player_transport = unknown
        return self.player_transport

    def damage_transport(self, condition=critical_damaged):
        self.transport_condition = condition

    # def new_transport(self, transport, condition=good_condition):
    #     self.player_transport = transport
    #     self.transport_condition = condition
    #     return self.player_transport

    def die(self, dead=dead):
        self.transport_condition = dead
        self.live = False

