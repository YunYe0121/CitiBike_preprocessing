import json
import numpy as np
import pandas as pd
from my_coordinate_transfer import coordinate_transfer

def haversine(lat_1, lng_1, lat_2, lng_2):
    from math import radians, sin, cos, atan2, sqrt
    lat_1, lng_1, lat_2, lng_2 = map(radians, [lat_1, lng_1, lat_2, lng_2])
    a = sin((lat_2 - lat_1) / 2) ** 2 + cos(lat_1) * cos(lat_2) * (sin((lng_2 - lng_1) / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c

def POI_generator():

    station_info_df = pd.read_csv('csv_files/station_info.csv')

    # the max distance use to search
    max_radius = 500
    # side length of grid
    grid_side_length = 5
    # num of station
    station_num = 1072

    # try to get all user rating's number and find the max and min
    rating_list = []
    user_ratings_total_list = []

    for index in range(1, station_num + 1):
        with open('json_files/s_' + str(index) + '.json', encoding = 'UTF-8') as data_f:
            data = json.load(data_f)
        for result in data['results']:
            if 'rating' in result and 'user_ratings_total' in result:
                rating_list.append( float(result.get('rating')) )
                user_ratings_total_list.append( int(result.get('user_ratings_total')) )

    max_user_rating_total = np.array( user_ratings_total_list ).max()
    min_user_rating_total = np.array( user_ratings_total_list ).min()

    print('max_user_rating_total:', max_user_rating_total)
    print('min_user_rating_total:', min_user_rating_total)

    POI = np.empty( (station_num, 10, grid_side_length, grid_side_length) )

    # according to rating and total rating number to calcuate POI value
    for index in range(1, station_num + 1):
        with open('json_files/s_' + str(index) + '.json', encoding = 'UTF-8') as data_f:
            data = json.load(data_f)

        s_lat = station_info_df.iloc[index - 1]['station_lat']
        s_lng = station_info_df.iloc[index - 1]['station_lng']

        with open('json_files/all_type_dict.json', encoding = 'UTF-8') as type_f:
            type_dict = json.load(type_f)

        my_map = np.zeros((10, grid_side_length, grid_side_length))
        type_table = {'food': 0, 'mall': 1, 'business': 2, 'hospital': 3, 'transpotation': 4, 'government': 5, 'park': 6, 'apartment': 7, 'entertainment': 8, 'sport': 9}

        for result in data['results']:
            
            if 'rating' in result and 'user_ratings_total' in result:

                p_lat = result['geometry']['location']['lat']
                p_lng = result['geometry']['location']['lng']

                x = round(haversine(s_lat, s_lng, s_lat, p_lng) * 1000)
                y = round(haversine(s_lat, s_lng, p_lat, s_lng) * 1000)

                c_x, c_y = coordinate_transfer(x, y, max_radius, grid_side_length)

                # d = haversine(s_lat, s_lng, p_lat, p_lng)
                # if d > (max_radius / 1000):
                #     continue

                # normaliztion for user_rating_total
                user_ratings_total_after_normalization = (int(result['user_ratings_total']) - min_user_rating_total) / (max_user_rating_total - min_user_rating_total)
                value = result['rating'] * user_ratings_total_after_normalization

                type_list = result['types']
                type_check = np.full(10, False, dtype = bool)

                for type in type_list:
                    if type_dict[type] != 'None' and type_check[type_table[type_dict[type]]] == False:
                        my_map[type_table[type_dict[type]]][c_x][c_y] += value
                        type_check[type_table[type_dict[type]]] = True

        # a simple test to check whethr grid array's values are all zeros
        all_zeros = not np.any(my_map)
        print('index: {}, my map all zeros:'.format(index), all_zeros)
        POI[index - 1] = my_map.copy()

    print('POI:')
    print(POI)
    print('POI.shape:')
    print(POI.shape)

    np.save('npy_files/POI.npy', POI)
