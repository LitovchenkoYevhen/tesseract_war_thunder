from time import sleep

from lxml import html
import requests as req
from settings import crowler_base_url
from tesseract_war_thunder.scan.services import player_dict


def crowl_and_set_player_stats(player):
    if player.raw_nick == 'AI':
        return
    nick = player.raw_nick
    if nick.startswith('⋇'):
        print(nick)
        nick = nick.strip('⋇') + '@psn'
    rek = req.get(crowler_base_url.format(player.player_nick))
    status_code = rek.status_code
    if status_code == 200:
        tree = html.fromstring(rek.content)
        elements = tree.xpath('.//div[@class = "col mycol text-center"]')
        stats_dict = {element.xpath('strong/text()')[0]: ''.join(element.xpath('.//div[@class = "kpd_value"]/text()'))
                      for element in elements}
        if stats_dict:
            player.update_stats(stats_dict)
        else:
            print(nick, 'NO stats', status_code)
            print(crowler_base_url.format(nick))


def crowl_list():
    while True:
        sleep(0.5)
        for player in player_dict.values():
            if not player.stats:
                crowl_and_set_player_stats(player)

