import numpy as np
import pandas as pd

from my_coordinate_transfer import coordinate_transfer

def haversine(lat_1, lng_1, lat_2, lng_2):
    from math import radians, sin, cos, atan2, sqrt
    lat_1, lng_1, lat_2, lng_2 = map(radians, [lat_1, lng_1, lat_2, lng_2])
    a = sin((lat_2 - lat_1) / 2) ** 2 + cos(lat_1) * cos(lat_2) * (sin((lng_2 - lng_1) / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c

def grid_array_generator():

    start_month = 7
    end_month = 8
    filter_num = 100
    grid_side_length = 7
    time_slot_num = (31 + 31) * 48

    # station_info
    station_info_df = pd.read_csv('csv_files/station_info.csv')
    print(station_info_df)

    station_name_list = station_info_df['station_name'].tolist()
    station_id_list = station_info_df['station_id'].tolist()
    station_lat_list = station_info_df['station_lat'].tolist()
    station_lng_list = station_info_df['station_lng'].tolist()

    # major_flow_station_info
    major_flow_station_info_df = pd.read_csv('csv_files/major_flow_station_info.csv')
    major_flow_station_name_list = major_flow_station_info_df['station_name'].tolist()
    major_flow_station_id_list = major_flow_station_info_df['station_id'].tolist()
    major_flow_station_index_list = major_flow_station_info_df['index'].tolist()
    major_flow_station_lat_list = []
    major_flow_station_lng_list = []
    for major_flow_station_index, major_flow_station_record in major_flow_station_info_df.iterrows():
        t_i = major_flow_station_record['index']
        major_flow_station_lat_list.append( station_lat_list[t_i] )
        major_flow_station_lng_list.append( station_lng_list[t_i] )

    # arriving_and_deaprting
    # arriving_and_deaprting = np.load('npy_files/arr_and_dep.npy')
    # print('arriving_and_deaprting:')
    # print(arriving_and_deaprting)
    # print('arriving_and_deaprting.shape:')
    # print(arriving_and_deaprting.shape)

    # rebal_flow
    # rebal_flow = np.load('npy_files/rebal_flow.npy')
    # print('rebal_flow:')
    # print(rebal_flow)
    # print('rebal_flow.shape:')
    # print(rebal_flow.shape)

    max_grid_distance_list = []
    total_cluster_list = []

    major_flow_df = pd.read_csv('csv_files/major_flow.csv')
    major_flow_df['Unnamed: 0'] = major_flow_df['Unnamed: 0'].astype(str)

    for month_number in range(0, end_month - start_month + 1):
        month_max_grid_distance_list = []
        month_cluster_list = []
        for major_flow_station_index in range(filter_num):

            start_index = month_number * filter_num + 1
            end_index = start_index + filter_num
            cluster_list = []

            find_area = major_flow_df.values[major_flow_station_index, start_index : end_index]

            # according to the observation, we find that most stations have a lot of records whose start station and end station are same
            # we want to focus on the relationship between stations, so we remove the value whose src and dst are identical
            find_area = np.delete(find_area, major_flow_station_index)
            max_flow_in_this_month = find_area.max()

            # we use max_flow_in_this_month's 50% to be threshold
            # plan B: quartile
            threshold = max_flow_in_this_month * 0.5

            # of couse, the station we search also will be a member in this cluster
            cluster_list.append(major_flow_station_index)
            # according to the threshold to choose current station's clusters
            for i in range(len(find_area)):
                if find_area[i] >= threshold:
                    if i >= major_flow_station_index:
                        cluster_list.append(i + 1)
                    else:
                        cluster_list.append(i)

            # calculate the distances between the current station and all clusters
            # find the max distance for the grid distance
            distance_list = []
            for cluster_index in cluster_list:
                d = haversine(major_flow_station_lat_list[major_flow_station_index], major_flow_station_lng_list[major_flow_station_index], major_flow_station_lat_list[cluster_index], major_flow_station_lng_list[cluster_index])
                distance_list.append(d)

            max_grid_distance = np.array(distance_list).max()
            month_max_grid_distance_list.append(max_grid_distance)
            month_cluster_list.append(cluster_list)
            
        max_grid_distance_list.append(month_max_grid_distance_list)
        total_cluster_list.append(month_cluster_list)

    # load scalar_inflow_and_outflow and scalar_volume
    scalar_inflow_and_outflow = np.load('npy_files/scalar_inflow_and_outflow.npy')
    scalar_volume = np.load('npy_files/scalar_volume.npy')

    # grid_inflow_and_ouflow
    grid_inflow_and_outflow = np.zeros((time_slot_num, filter_num, 2, grid_side_length, grid_side_length), dtype = 'int32')
    # grid_volume
    grid_volume = np.zeros( (time_slot_num, filter_num, 2, grid_side_length, grid_side_length), dtype = 'int32' )

    for time_slot_index in range(time_slot_num):

        print('time_slot_index:', time_slot_index)

        for current_station_index in range(filter_num):

            if time_slot_index >= 0 and time_slot_index < 1488:
                month = 7
            elif time_slot_index >= 1488 and time_slot_index < 2976:
                month = 8

            # we want to point out cluster's inflow and outflow in the grid
            # read each cluster's inflow and outflow and specific time slot
            max_grid_distance = (max_grid_distance_list[month - start_month][current_station_index]) * 1000
            cluster_list = total_cluster_list[month - start_month][current_station_index]

            for cluster_index in cluster_list:
                x = round(haversine(major_flow_station_lat_list[current_station_index], major_flow_station_lng_list[current_station_index], major_flow_station_lat_list[current_station_index], major_flow_station_lng_list[cluster_index]) * 1000)
                y = round(haversine(major_flow_station_lat_list[current_station_index], major_flow_station_lng_list[current_station_index], major_flow_station_lat_list[cluster_index], major_flow_station_lng_list[current_station_index]) * 1000)

                c_x, c_y = coordinate_transfer(x, y, max_grid_distance, grid_side_length)

                # inflow
                grid_inflow_and_outflow[time_slot_index, current_station_index, 0, c_x, c_y] += scalar_inflow_and_outflow[time_slot_index, cluster_index, 0]

                # outflow
                grid_inflow_and_outflow[time_slot_index, current_station_index, 1, c_x, c_y] += scalar_inflow_and_outflow[time_slot_index, cluster_index, 1]

                # volume
                grid_volume[time_slot_index, current_station_index, 0, c_x, c_y] += scalar_volume[time_slot_index, cluster_index, 0]
                grid_volume[time_slot_index, current_station_index, 1, c_x, c_y] += scalar_volume[time_slot_index, cluster_index, 1]

    print('grid_inflow_and_outflow:')
    print(grid_inflow_and_outflow)
    print('grid_inflow_and_outflow.shape:')
    print(grid_inflow_and_outflow.shape)

    print('grid_volume:')
    print(grid_volume)
    print('grid_volume.shape:')
    print(grid_volume.shape)

    np.save('npy_files/grid_inflow_and_outflow.npy', grid_inflow_and_outflow)
    np.save('npy_files/grid_volume.npy', grid_volume)

if __name__ == '__main__':
    grid_array_generator()
