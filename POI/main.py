from station_info_generator import station_info_generator
from Google_Places_API_crawler import Google_Places_API_crawler
from type_collector import type_collector
from POI_generator import POI_generator
from data_min_max_checker import data_min_max_checker

if __name__ == '__main__':
    # Google_Places_API_crawler()
    # type_collector()
    station_info_generator()
    POI_generator()
    data_min_max_checker()
