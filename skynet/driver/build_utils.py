from IPython import embed
import pandas as pd
import numpy as np

# EDIT THIS
base_production_data = {'lumber': 623, 'clay': 749, 'iron': 560, 'wheat': 903}
mill_production_data = {'lumber': 1, 'clay': 1, 'iron': 1, 'wheat': 1.15}
hero_production_base_rate = 640
population_consumption_rate = -373
troop_consumption_rate = -683

cost_data = {'lumber': 9115, 'clay': 8725, 'iron': 9115, 'wheat': 3125}
current_resource_data = {'lumber': 7415, 'clay': 9305, 'iron': 7903, 'wheat': 3613}

# LEAVE THIS ALONE
DEFAULT_INDEX = pd.Index(['lumber', 'clay', 'iron', 'wheat'])

base_production_rates = pd.Series(name='base_production_rate', data=base_production_data, index=DEFAULT_INDEX)
oases_production_bonuses = pd.Series(name='oases_production_bonus', data={'lumber': 1, 'clay': 1, 'iron': 1, 'wheat': 1}, index=DEFAULT_INDEX)
mill_production_bonuses = pd.Series(name='mill_production_bonus', data=mill_production_data, index=DEFAULT_INDEX)

hero_production_bonuses_split = pd.Series(name='split', data={'lumber': (hero_production_base_rate*0.3), 'clay': (hero_production_base_rate*0.3), 'iron': (hero_production_base_rate*0.3), 'wheat': ((hero_production_base_rate*0.3)+6)}, index=DEFAULT_INDEX)
hero_production_bonuses_lumber = pd.Series(name='lumber', data={'lumber': hero_production_base_rate, 'clay': 0, 'iron': 0, 'wheat': 6}, index=DEFAULT_INDEX)
hero_production_bonuses_clay = pd.Series(name='clay', data={'lumber': 0, 'clay': hero_production_base_rate, 'iron': 0, 'wheat': 6}, index=DEFAULT_INDEX)
hero_production_bonuses_iron = pd.Series(name='iron', data={'lumber': 0, 'clay': 0, 'iron': hero_production_base_rate, 'wheat': 6}, index=DEFAULT_INDEX)
hero_production_bonuses_wheat = pd.Series(name='wheat', data={'lumber': 0, 'clay': 0, 'iron': 0, 'wheat': (hero_production_base_rate+6)}, index=DEFAULT_INDEX)
hero_production_bonuses = pd.concat([hero_production_bonuses_split, hero_production_bonuses_lumber, hero_production_bonuses_clay, hero_production_bonuses_iron, hero_production_bonuses_wheat], axis=1)
plus_production_bonuses = pd.Series(name='plus_production_bonus', data={'lumber': 1.25, 'clay': 1.25, 'iron': 1.25, 'wheat': 1.25}, index=DEFAULT_INDEX)

population_production_rates = pd.Series(name='population_production_rate', data={'lumber': 0, 'clay': 0, 'iron': 0, 'wheat': population_consumption_rate}, index=DEFAULT_INDEX)
troop_production_rates = pd.Series(name='troop_production_rate', data={'lumber': 0, 'clay': 0, 'iron': 0, 'wheat': troop_consumption_rate}, index=DEFAULT_INDEX)

costs = pd.Series(name='cost', data=cost_data, index=DEFAULT_INDEX)
current_resources = pd.Series(name='cost', data=current_resource_data, index=DEFAULT_INDEX)
deficits = (costs - current_resources).apply(lambda n: max(0, n))
# END OF LEAVE ALONE SECTION

def production_rates_for_hero_production_setting(hero_production_setting):
    free_production_rates = (base_production_rates * oases_production_bonuses * mill_production_bonuses).rename('free_production_rate')
    interim_production_rates = ((free_production_rates + hero_production_bonuses[hero_production_setting]) * plus_production_bonuses).rename('interim_production_rate')
    production_rates = (interim_production_rates + troop_production_rates + population_production_rates).rename('production_rate')
    return production_rates

def get_best_hero_production_setting_simple():
    hours_till_ready_data = {}
    for hero_production_setting in ['split', 'lumber', 'clay', 'iron', 'wheat']:
        production_rates = production_rates_for_hero_production_setting(hero_production_setting)
        hours_till_ready_data[hero_production_setting] = (deficits / production_rates).max()

    hours_till_ready = pd.Series(name='hours_till_ready', data=hours_till_ready_data)
    return hours_till_ready.idxmin()

get_best_hero_production_setting = get_best_hero_production_setting_simple

embed()


