from station_info_generator import station_info_generator
from fdata_and_vdata_maker import fdata_and_vdata_maker
from dataset_splitter import dataset_splitter
from data_min_max_checker import data_min_max_checker

if __name__ == '__main__':
    station_info_generator()
    fdata_and_vdata_maker()
    dataset_splitter()
    data_min_max_checker()
