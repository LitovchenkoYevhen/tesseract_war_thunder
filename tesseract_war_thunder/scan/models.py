
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

