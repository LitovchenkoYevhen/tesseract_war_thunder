import os
from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent


# SCREENSHOTS_PATH = os.path.join(BASE_DIR, 'screenshots/')
tesseract_conf = r'--oem 3 --psm 6'

code_dict = {
    'kill': 'сбил',
    'crashed': 'разбился'
}

action_dict = {
    'kill': 'сбил',
    'damaged': 'подбил',
    'arson': 'поджог',
    'destroy': 'уничтожил',
    'crashed': 'разбился'
}

frequency = 1  # Frequency of requests to war thunder api.
match_percent = 90  # Describes percent to consider match as success.

debug = True

crowler_base_url = 'https://thunderskill.com/ru/stat/{}'