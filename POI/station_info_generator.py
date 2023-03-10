import numpy as np
import pandas as pd

def station_info_generator():

    start_month = 7
    end_month = 8

    df_list = []
    for i in range(start_month, end_month + 1):
        df_temp = pd.read_csv( 'csv_files/2020%02d-citibike-tripdata.csv' % i, low_memory = False )
        df_list.append(df_temp)

    station_list = []

    for i in range(0, end_month - start_month + 1):
        df_list[i] = df_list[i].drop( columns = ['tripduration', 'starttime', 'stoptime', 'bikeid', 'usertype', 'birth year', 'gender'] )
        print('size of df_list[' + str(i) + ']: ', df_list[i].shape)
        df_list[i] = df_list[i].drop_duplicates()
        print('After drop_duplicates():')
        print('size of df_list[' + str(i) + ']: ', df_list[i].shape)
        print()

    station_dict = { 'station_id' : [], 'station_name' : [], 'station_lat' : [], 'station_lng' : [] }
    station_pd = pd.DataFrame(station_dict)

    # print(station_pd)

    for i in range(0, end_month - start_month + 1):
        station_id_list = df_list[i]['start station id'].tolist() + df_list[i]['end station id'].tolist()
        station_name_list = df_list[i]['start station name'].tolist() + df_list[i]['end station name'].tolist()
        station_lat_list = round(df_list[i]['start station latitude'], 6).tolist() + round(df_list[i]['end station latitude'], 6).tolist()
        station_lng_list = round(df_list[i]['start station longitude'], 6).tolist() + round(df_list[i]['end station longitude'], 6).tolist()

        station_pd_temp = pd.DataFrame()
        station_pd_temp['station_id'] = station_id_list
        station_pd_temp['station_name'] = station_name_list
        station_pd_temp['station_lat'] = station_lat_list
        station_pd_temp['station_lng'] = station_lng_list

        if i == 0:
            station_pd = station_pd_temp
        else:
            station_pd = pd.concat([station_pd, station_pd_temp])

    station_pd = station_pd.dropna()
    station_pd['station_id'] = station_pd['station_id'].astype(str)
    station_pd = station_pd.sort_values(by = 'station_id')
    station_pd = station_pd.drop_duplicates(subset = 'station_id')
    station_pd = station_pd.reset_index(drop = True, inplace = False)

    print(station_pd)
    print(station_pd.shape)

    station_pd.to_csv('csv_files/station_info.csv')

if __name__ == '__main__':
    station_info_generator()
