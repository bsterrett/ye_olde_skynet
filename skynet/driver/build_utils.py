from __future__ import division
from functools import partial
from IPython import embed
from scipy.optimize import minimize
import numpy as np
import pandas as pd

# EDIT THIS
base_production_data = {'lumber': 623, 'clay': 749, 'iron': 560, 'wheat': 903}
mill_production_data = {'lumber': 1, 'clay': 1.15, 'iron': 1, 'wheat': 1.2}
oases_production_data = {'lumber': 1.25, 'clay': 1, 'iron': 1, 'wheat': 1.25}
hero_production_base_rate = 640
population_consumption_rate = -373
troop_consumption_rate = -683

cost_data = {'lumber': 9115, 'clay': 8725, 'iron': 9115, 'wheat': 3125}
current_resource_data = {'lumber': 7415, 'clay': 9305, 'iron': 7903, 'wheat': 3613}

# LEAVE THIS ALONE
DEFAULT_INDEX = pd.Index(['lumber', 'clay', 'iron', 'wheat'])

base_production_rates = pd.Series(name='base_production_rate', data=base_production_data, index=DEFAULT_INDEX)
oases_production_bonuses = pd.Series(name='oases_production_bonus', data=oases_production_data, index=DEFAULT_INDEX)
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

def get_time_given_hero_production_setting_allocations(allocations):
    split_allocation, lumber_allocation, clay_allocation, iron_allocation, wheat_allocation = allocations
    production = pd.Series(name='production', data={'lumber': 0, 'clay': 0, 'iron': 0, 'wheat': 0}, index=DEFAULT_INDEX)
    production += production_rates_for_hero_production_setting('split') * split_allocation
    production += production_rates_for_hero_production_setting('lumber') * lumber_allocation
    production += production_rates_for_hero_production_setting('clay') * clay_allocation
    production += production_rates_for_hero_production_setting('iron') * iron_allocation
    production += production_rates_for_hero_production_setting('wheat') * wheat_allocation
    return (deficits / production).max()

def allocations_sum_to_one(*allocations):
    return sum(*allocations) - 1

constraints = [{'type': 'eq', 'fun': allocations_sum_to_one}]
x0 = [0.2] * 5
bounds = [(0,1)] * 5

optimization_results = minimize(get_time_given_hero_production_setting_allocations, x0=x0, bounds=bounds, constraints=constraints)

def normalize_optimized_allocations(allocations):
    def round_small_value_to_zero(value):
        if abs(value) <= 1e-15:
            return 0
        return value

    rounded_allocations = map(round_small_value_to_zero, allocations)
    rounded_allocation_sum = sum(rounded_allocations)
    normalize_allocations = map(lambda r: r/rounded_allocation_sum, rounded_allocations)
    return normalize_allocations

def optimized_hourly_allocations(optimization_results):
    allocations = optimization_results.x
    normalized_allocations = normalize_optimized_allocations(allocations)
    hourly_allocation_values = map(lambda a: a*optimization_results.fun, normalized_allocations)
    hourly_allocation_keys = ['split', 'lumber', 'clay', 'iron', 'wheat']
    hourly_allocations = {k: v for (k,v) in zip(hourly_allocation_keys, hourly_allocation_values)}
    return hourly_allocations

print(optimized_hourly_allocations(optimization_results))
