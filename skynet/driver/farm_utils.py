from functools import partial
from IPython import embed
from json import load
from scipy.spatial.distance import euclidean
import pandas as pd

def troop_allotment_list_to_dataframe(allotment_list):
    allotments = pd.DataFrame(columns=['troop_specifier', 'count'], data=allotment_list)
    return allotments

def coordinates_to_distance(movements, origin_point):
    coordinates = pd.Series(name='coordinates', data=zip(movements.x_coordinate.tolist(), movements.y_coordinate.tolist()))
    for i in coordinates.index:
        # check that concatenated coordinates have the same indices as the originals
        assert coordinates.iloc[i] == (movements.x_coordinate.iloc[i], movements.y_coordinate.iloc[i])
    euclidean_partial = partial(euclidean, v=origin_point)
    distances = coordinates.rename('distance').apply(euclidean_partial)
    return distances

def convert_options_json_to_dataframe(options_json):
    movements = pd.DataFrame(data=options_json)
    movements['troop_allotments'] = movements['troop_allotments'].apply(troop_allotment_list_to_dataframe).fillna(value=0)
    movements['distance'] = coordinates_to_distance(movements, (45, 30))
    return movements

with open('data/farm_options_list.json', 'r') as farm_options_file_handle:
    options_json = load(farm_options_file_handle)

movements = convert_options_json_to_dataframe(options_json)
embed()
