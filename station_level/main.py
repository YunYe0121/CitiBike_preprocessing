from station_info_generator import station_info_generator
from arr_and_dep_generator import arr_and_dep_generator
from rebal_flow_generator import rebal_flow_generator
from major_flow_generator import major_flow_generator
from scalar_array_generator import scalar_array_generator
from grid_array_generator import grid_array_generator
from data_min_max_checker import data_min_max_checker
from dataset_splitter import dataset_splitter

if __name__ == '__main__':
    station_info_generator()
    arr_and_dep_generator()
    rebal_flow_generator()
    major_flow_generator()
    scalar_array_generator()
    grid_array_generator()
    dataset_splitter()
    data_min_max_checker()
