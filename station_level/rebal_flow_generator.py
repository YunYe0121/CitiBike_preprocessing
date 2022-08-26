import numpy as np
import pandas as pd

def rebal_flow_generator():

    start_month = 7
    end_month = 8
    time_slot_num = (31 + 31) * 48
    station_num = 1072

    station_info_df = pd.read_csv('csv_files/station_info.csv')
    print(station_info_df)

    station_name_list = station_info_df['station_name'].tolist()
    station_id_list = station_info_df['station_id'].tolist()
    station_lat_list = station_info_df['station_lat'].tolist()
    station_lng_list = station_info_df['station_lng'].tolist()

    # in/arriving is 0, out/departing is 1
    rebal_flow = np.zeros( (time_slot_num, station_num, 2), dtype = 'int32')

    for month_number in range(start_month, end_month + 1):

        print('Dealing with: csv_files/2020%02d-citibike-tripdata.csv' % month_number)
        df = pd.read_csv('csv_files/2020%02d-citibike-tripdata.csv' % month_number, low_memory = False, usecols = ['starttime', 'start station id', 'stoptime', 'end station id', 'bikeid'], parse_dates = ['starttime', 'stoptime'])

        df.info()

        dfbike = df.sort_values(by = ['bikeid', 'starttime', 'stoptime'])
        print(dfbike.head(10))

        offset = pd.DataFrame( {'starttime' : pd.to_datetime('2010-07-01'), 'start station id' : 0, 'stoptime' : pd.to_datetime('2010-07-01'), 'end station id' : 0,'bikeid' : 0}, index = [0] )

        dfbike_1 = pd.concat([offset, dfbike]).reset_index(drop = True)
        dfbike_2 = pd.concat([dfbike, offset]).reset_index(drop = True)

        dfbike = pd.concat( [dfbike_1[['bikeid', 'stoptime', 'end station id']], dfbike_2[['bikeid', 'starttime', 'start station id']]], axis = 1 )

        print(dfbike.head(10))

        dfbike.columns = ['bikeid_1', 'starttime', 'start station id', 'bikeid_2', 'stoptime', 'end station id'] 

        dfrebal = dfbike[ ['starttime', 'start station id', 'stoptime', 'end station id'] ].loc[ (dfbike.bikeid_1 == dfbike.bikeid_2) & (dfbike['start station id'] != dfbike['end station id']) ] 

        dfrebal.reset_index(drop = True, inplace = True)

        print(dfrebal)

        for record_index, record in dfrebal.iterrows():
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
            rebal_flow[start_time_slot_index, start_station_index, 1] += 1

            # inflow / arriving
            rebal_flow[end_time_slot_index, end_station_index, 0] += 1

    print('rebal_flow:')
    print(rebal_flow)
    print('rebal_flow.shape:')
    print(rebal_flow.shape)

    np.save('npy_files/rebal_flow.npy', rebal_flow)

if __name__ == '__main__':
    rebal_flow_generator()
