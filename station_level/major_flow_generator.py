import numpy as np
import pandas as pd

def haversine(lat_1, lng_1, lat_2, lng_2):
    from math import radians, sin, cos, atan2, sqrt
    lat_1, lng_1, lat_2, lng_2 = map(radians, [lat_1, lng_1, lat_2, lng_2])
    a = sin((lat_2 - lat_1) / 2) ** 2 + cos(lat_1) * cos(lat_2) * (sin((lng_2 - lng_1) / 2) ** 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return 6371 * c

def take_second_element(arg):
    return arg[1]

def major_flow_generator():

    # load station info
    station_info_df = pd.read_csv('csv_files/station_info.csv')
    print(station_info_df)

    station_name_list = station_info_df['station_name'].tolist()
    station_id_list = station_info_df['station_id'].tolist()
    station_lat_list = station_info_df['station_lat'].tolist()
    station_lng_list = station_info_df['station_lng'].tolist()

    station_num = 1072

    start_month = 7
    end_month = 8

    flow_array = np.zeros((end_month - start_month + 1, station_num, station_num), dtype = 'int32')

    # get record data
    for month_number in range(start_month, end_month + 1):

        print('Dealing with: csv_files/2020%02d-citibike-tripdata.csv' % month_number)
        month_df = pd.read_csv('csv_files/2020%02d-citibike-tripdata.csv' % month_number, low_memory = False)
        month_df = month_df.dropna(axis = 0, subset = ['start station name', 'end station name', 'start station id', 'end station id'])
        # month_df['start_station_id'] = month_df['start_station_id'].astype(str)
        # month_df['end_station_id'] = month_df['end_station_id'].astype(str)

        for record_index, record in month_df.iterrows():

            print('record_index:', record_index)

            start_station_index = station_id_list.index( record['start station id'] )
            end_station_index = station_id_list.index( record['end station id'] )
            start_time = pd.to_datetime( record['starttime'], format = '%Y-%m-%d %H:%M:%S' )
            end_time = pd.to_datetime( record['stoptime'], format = '%Y-%m-%d %H:%M:%S' )

            start_time_day_index = 0
            if start_time.month == 7:
                start_time_day_index += 0
            elif start_time.month == 8:
                start_time_day_index += 31
            start_time_day_index += (start_time.day - 1)
            start_time_slot_index = (start_time_day_index * 48 + start_time.hour * 2 + (1 if start_time.minute >= 30 else 0))

            end_time_day_index = 0
            if end_time.month == 7:
                end_time_day_index += 0
            elif end_time.month == 8:
                end_time_day_index += 31
            end_time_day_index += (end_time.day - 1)
            end_time_slot_index = (end_time_day_index * 48 + end_time.hour * 2 + (1 if end_time.minute >= 30 else 0))

            flow_array[month_number - start_month][start_station_index][end_station_index] += 1

    print('flow_array:')
    print(flow_array)

    # calculate inflow and outflow
    inflow_array = flow_array.sum(axis = 1)
    outflow_array = flow_array.sum(axis = 2)

    print('inflow_array:')
    print(inflow_array)
    print('inflow_array.shape')
    print(inflow_array.shape)
    print('outflow_array:')
    print(outflow_array)
    print('outflow_array.shape')
    print(outflow_array.shape)

    # calculate total flow
    total_flow_array = np.full((end_month - start_month + 1, station_num), fill_value = -1, dtype = 'int32')
    for month in range(0, end_month - start_month + 1):
        for i in range(station_num):
            total_flow_array[month, i] = inflow_array[month, i] + outflow_array[month, i]

    print('total_flow_array:')
    print(total_flow_array)

    # sort and find the major flow and stations
    total_flow_sorted_list = []
    for index in range(station_num):
        temp = []
        temp.append(index)
        temp_sum = 0
        for i in range(0, end_month - start_month + 1):
            temp_sum += total_flow_array[i, index]
        temp.append(temp_sum)
        temp.append(station_id_list[index])
        temp.append(station_name_list[index])
        total_flow_sorted_list.append(temp)

    # filter the major flow
    total_flow_sorted_list.sort(key = take_second_element, reverse = True)

    print('total_flow_sorted_list:')
    print(total_flow_sorted_list)

    filter_num = 100
    major_flow_array = np.full((end_month - start_month + 1, filter_num * 2, filter_num * 2), fill_value = -1, dtype = 'int32')

    # create major flow array
    for i in range(filter_num * 2):
        src_station_index = total_flow_sorted_list[i][0]
        for j in range(filter_num * 2):
            dst_station_index = total_flow_sorted_list[j][0]
            for month in range(0, end_month - start_month + 1):
                major_flow_array[month, i, j] = flow_array[month, src_station_index, dst_station_index]        

    major_flow_station_name_list = []
    column_list = list(map(str, list(np.arange(filter_num * 2))))
    month_name_list = ['July', 'August']

    for i in range(filter_num * 2):
        major_flow_station_name_list.append( total_flow_sorted_list[i][3] )

    print('major_flow_station_name_list:')
    print(major_flow_station_name_list)

    for month in range(0, end_month - start_month + 1):

        month_column_list = list(map(lambda column_list_element: month_name_list[month] + '_' + column_list_element, column_list))

        if month == 0:
            major_df = pd.DataFrame(major_flow_array[month], index = major_flow_station_name_list, columns = month_column_list)
        else:
            temp_df = pd.DataFrame(major_flow_array[month], index = major_flow_station_name_list, columns = month_column_list)
            major_df = pd.concat([major_df, temp_df], axis = 1)

    # save data as csv file
    print('major_flow_df:')
    print(major_df)
    major_df.to_csv('csv_files/major_flow.csv')

    major_flow_station_info_list = total_flow_sorted_list[: filter_num * 2]
    major_flow_station_info_df = pd.DataFrame(major_flow_station_info_list, columns = ['index', 'total_flow', 'station_id', 'station_name'])
    print('major_flow_station_info_df:')
    print(major_flow_station_info_df)
    major_flow_station_info_df.to_csv('csv_files/major_flow_station_info.csv')

if __name__ == '__main__':
    major_flow_generator()
