import cv2
import pytesseract
import mss
import re
from time import sleep

from tesseract_war_thunder.scan.settings import debug, tesseract_conf
from tesseract_war_thunder.scan import variables

screen_dict = {
    'alias': {"top": 260, "left": 490, "width": 210, "height": 320},
    'enemy': {"top": 260, "left": 740, "width": 210, "height": 320}
}


def make_players_dict():
    players_dict = {}
    for team_key, team_value in zip(screen_dict.keys(), screen_dict.values()):
        players_dict[team_key] = []
        file_name = "{}_screenshot.png".format(team_key)
        with mss.mss() as sct:
            # The screen part to capture
            # Grab the data
            # sleep(3)
            if not debug:
                screenshot = sct.grab(team_value)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=file_name)
        img = cv2.imread(file_name)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 3)
        # cv2.imshow('Result', gray)
        # cv2.waitKey(0)
        str_img = pytesseract.image_to_string(gray, config=tesseract_conf)
        for line in str_img.splitlines():
            if line:
                line = line.strip()
                line = re.search(r'\w+$', line)[0]
                players_dict[team_key].append(line)
        variables.alias_list = players_dict['alias']
        variables.enemy_list = players_dict['enemy'] if 'enemy' in players_dict.keys() else None
    return players_dict



