import numpy as np
import pandas as pd

def arr_and_dep_generator():

    station_info_df = pd.read_csv('csv_files/station_info.csv')
    print(station_info_df)

    station_name_list = station_info_df['station_name'].tolist()
    station_id_list = station_info_df['station_id'].tolist()
    station_lat_list = station_info_df['station_lat'].tolist()
    station_lng_list = station_info_df['station_lng'].tolist()

    start_month = 7
    end_month = 8
    time_slot_num = (31 + 31) * 48
    station_num = 1072

    # 0 is inflow, 1 is outflow
    arr_and_dep = np.zeros( (time_slot_num, station_num, 2), dtype = 'int32')

    for month_number in range(start_month, end_month + 1):
        print('Dealing with: csv_files/2020%02d-citibike-tripdata.csv' % month_number)
        month_df = pd.read_csv('csv_files/2020%02d-citibike-tripdata.csv' % month_number, low_memory = False)
        month_df = month_df.dropna(axis = 0, subset = ['start station name', 'end station name', 'start station id', 'end station id'])
        # month_df['start station id'] = month_df['start station id'].astype(str)
        # month_df['end station id'] = month_df['end station id'].astype(str)

        for record_index, record in month_df.iterrows():

            # show the record_index
            print('reconrd_index:', record_index)

            # calculate start time slot index
            start_time = pd.to_datetime(record['starttime'], format = '%Y-%m-%d %H:%M:%S')
            start_time_day_index = 0

            if start_time.month == 7:
                start_time_day_index += 0
            elif start_time.month == 8:
                start_time_day_index += 31
            
            start_time_day_index += (start_time.day - 1)
            start_time_slot_index = (start_time_day_index * 48 + start_time.hour * 2 + (1 if start_time.minute >= 30 else 0))

            # calculate end time slot index
            end_time = pd.to_datetime(record['stoptime'], format = '%Y-%m-%d %H:%M:%S')
            end_time_day_index = 0

            if end_time.month == 7:
                end_time_day_index += 0
            elif end_time.month == 8:
                end_time_day_index += 31

            end_time_day_index += (end_time.day - 1)
            end_time_slot_index = (end_time_day_index * 48 + end_time.hour * 2 + (1 if end_time.minute >= 30 else 0))

            # find start station index
            start_station_index = station_id_list.index( record['start station id'] )

            # find end station index
            end_station_index = station_id_list.index( record['end station id'] )

            # outflow / departing
            arr_and_dep[start_time_slot_index, start_station_index, 1] += 1

            # inflow / arriving
            arr_and_dep[end_time_slot_index, end_station_index, 0] += 1

    print('arr_and_dep:')
    print(arr_and_dep)
    print('arr_and_dep.shape:')
    print(arr_and_dep.shape)

    np.save('npy_files/arr_and_dep.npy', arr_and_dep)

if __name__ == '__main__':
    arr_and_dep_generator()
