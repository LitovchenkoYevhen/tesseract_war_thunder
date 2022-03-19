
class Player:
    good_condition = 'not damaged'
    critical_damaged = 'has been crited'
    unknown = 'unknown'
    dead = 'dead'

    def __init__(self, player, transport, nick, raw_nick=None, enemy=None, stats=None, condition=good_condition):
        self.player_name = player
        self.player_nick = nick
        self.player_transport = transport
        self.transport_condition = condition
        self.live = True
        self.enemy = enemy
        self.stats = stats
        self.raw_nick = raw_nick

    def __str__(self):
        return self.player_name + ' ' + self.player_transport + ' ' + self.transport_condition

    def destroy_transport(self, unknown):
        self.player_transport = unknown
        return self.player_transport

    def damage_transport(self, condition=critical_damaged):
        self.transport_condition = condition

    def update_stats(self, stats_dict):
        self.stats = stats_dict


    # def new_transport(self, transport, condition=good_condition):
    #     self.player_transport = transport
    #     self.transport_condition = condition
    #     return self.player_transport

    def die(self, dead=dead):
        self.transport_condition = dead
        self.live = False

