from lxml import html
import requests as req
from settings import crowler_base_url


def crowl_player_stats(player_name):
    rek = req.get(crowler_base_url.format(player_name))
    if rek.status_code == 200:
        # print(crowler_base_url.format(player_name))

        tree = html.fromstring(rek.content)
        elements = tree.xpath('.//div[@class = "col mycol text-center"]')
        stats_dict = {element.xpath('strong/text()')[0]: ''.join(element.xpath('.//div[@class = "kpd_value"]/text()'))
                      for element in elements}
        return stats_dict




