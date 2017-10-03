from IPython import embed
from time import sleep
import humanlike_pauses
import json
import pages
import travian_driver
import random

import models
from models import player, base

with open('secrets.json', 'r') as secrets_file_handle:
    secrets = json.load(secrets_file_handle)

driver = travian_driver.TravianDriver(secrets['base_url'])
login_page = pages.LoginPage(driver)
generic_ui = pages.GeneralUIPage(driver)
send_troops_page = pages.SendTroopsPage(driver)

if not driver.is_user_logged_in():
    login_page.authenticate(secrets['username'], secrets['password'])

with open('farm_options_list.json', 'r') as farm_options_file_handle:
    farm_options_list = json.load(farm_options_file_handle)

filtered_farm_options_list = [options for options in farm_options_list if options['player'] not in ['gdonald']]
random.shuffle(filtered_farm_options_list)

# for farm_options in filtered_farm_options_list:
#     driver.send_troops(farm_options)

# gdonald_followup_raid = {
#     "action_type": "raid",
#     "player": "gdonald",
#     "troop_allotments": [
#         {
#             "count": 85,
#             "troop_specifier": "t1"
#         }
#     ],
#     "x_coordinate": 49,
#     "y_coordinate": 38
# }

# driver.send_troops(gdonald_followup_raid)

embed()
